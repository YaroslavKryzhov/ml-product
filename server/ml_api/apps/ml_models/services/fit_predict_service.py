import traceback
import functools
from typing import List, Tuple, Any

from beanie import PydanticObjectId

from ml_api.apps.ml_models import specs, errors, schemas
from ml_api.apps.ml_models.model import ModelMetadata
from ml_api.apps.ml_models.services.processors.composition_trainer import \
    CompositionValidationService
from ml_api.apps.ml_models.services.processors.model_construstor import \
    ModelConstructorService
from ml_api.apps.ml_models.services.processors.model_trainer import ModelTrainerService
from ml_api.apps.ml_models.services.processors.model_predictor import \
    ModelPredictorService
from ml_api.apps.ml_models.services.processors.params_validator import \
    ParamsValidationService
from ml_api.apps.ml_models.services.processors.composition_validator import \
    CompositionParamsValidator
from ml_api.apps.ml_models.services.processors.composition_constructor import \
    CompositionConstructorService
from ml_api.apps.ml_models.services.model_service import ModelService
from ml_api.apps.ml_models.repositories.repository_manager import \
    ModelRepositoryManager
from ml_api.apps.training_reports.services.report_creator import ReportCreatorService
from ml_api.apps.dataframes.facade import DataframeServiceFacade


def handle_exceptions(method):
    @functools.wraps(method)
    async def wrapper(self, model_meta, *args, **kwargs):
        try:
            return await method(self, model_meta, *args, **kwargs)
        except Exception as err:
            await self._process_error(model_meta, err)
            raise
    return wrapper


class ModelFitPredictService:
    """
    Отвечает за обработку запросов на обучение и предсказание моделей.
    """
    def __init__(self, user_id):
        self._user_id = user_id
        self.repository = ModelRepositoryManager(self._user_id)
        self.dataframe_service = DataframeServiceFacade(self._user_id)
        self.model_service = ModelService(self._user_id)

    async def _set_status(self, model_meta: ModelMetadata,
                          status: specs.ModelStatuses):
        await self.repository.set_status(model_meta.id, status)

    async def _process_error(self, model_meta, err):
        await self._set_status(model_meta, specs.ModelStatuses.PROBLEM)
        error_description = traceback.format_exc()
        report = ReportCreatorService().get_error_report(model_meta.task_type,
                                                         error_description)
        await self.model_service.add_report(model_meta.id,
                                            model_meta.dataframe_id, report)

    async def check_prediction_filename(self, filename: str):
        return await self.dataframe_service.check_prediction_filename(filename)

    @handle_exceptions
    async def train_model(self, model_meta: ModelMetadata) -> ModelMetadata:
        await self._set_status(model_meta, specs.ModelStatuses.BUILDING)
        validated_params = await self._prepare_params(model_meta)
        await self.repository.set_model_params(model_meta.id, validated_params)
        model = await self._prepare_model(model_meta, validated_params)
        features, target = await self._prepare_fit_data(model_meta)
        await self._set_status(model_meta, specs.ModelStatuses.TRAINING)
        training_results = await self._fit_model(model_meta, model, features, target)
        await self._save_training_results(model_meta, training_results)
        await self._set_status(model_meta, specs.ModelStatuses.TRAINED)
        return await self.repository.get_model_meta(model_meta.id)

    async def _prepare_params(self, model_meta: ModelMetadata):
        return await ParamsValidationService(
            self._user_id, model_meta).validate_params()

    async def _prepare_model(self, model_meta: ModelMetadata, validated_params):
        return ModelConstructorService().get_model(
            model_meta.task_type, validated_params)

    async def _prepare_fit_data(self, model_meta: ModelMetadata):
        if model_meta.task_type in [specs.AvailableTaskTypes.CLASSIFICATION,
                                    specs.AvailableTaskTypes.REGRESSION]:
            return await self.dataframe_service.\
                get_feature_target_df_supervised(model_meta.dataframe_id)
        else:
            return await self.dataframe_service.get_feature_target_df(
                model_meta.dataframe_id)

    async def _fit_model(self, model_meta: ModelMetadata, model, features,
                         target):
        return await ModelTrainerService(model_meta, model
                                         ).train_model(features, target)

    async def _save_training_results(self, model_meta: ModelMetadata,
                                     results: schemas.ModelTrainingResults):
        """Store trained model and related reports/predictions."""
        await self.repository.save_new_model(model_meta.id, results.model)
        for report, pred_df in results.results:
            await self.model_service.add_report(model_meta.id,
                                                model_meta.dataframe_id,
                                                report)
            filename = f"{model_meta.filename}_predictions" \
                       f"_{report.report_type.value}"
            await self.model_service.add_predictions(model_meta.id, pred_df,
                                                     filename)

    @handle_exceptions
    async def train_composition(self, composition_meta: ModelMetadata
                                ) -> ModelMetadata:
        await self._set_status(composition_meta, specs.ModelStatuses.BUILDING)
        validated_params = await self._prepare_composition_params(
            composition_meta)
        await self.repository.set_model_params(
            composition_meta.id, validated_params)
        estimators = await self._load_models(composition_meta)
        composition = await self._prepare_composition(
            composition_meta, validated_params, estimators)
        features, target = await self._prepare_fit_data(composition_meta)
        await self._set_status(composition_meta, specs.ModelStatuses.TRAINING)
        validation_results = await self._validate_composition(
            composition_meta, composition, features, target)
        await self._save_training_results(composition_meta, validation_results)
        await self._set_status(composition_meta, specs.ModelStatuses.TRAINED)
        return await self.repository.get_model_meta(composition_meta.id)

    async def _load_single_model(self, model_id):
        model_meta = await self.repository.get_model_meta(model_id)
        model = await self.repository.load_model(model_id)
        model_name = f"{model_meta.model_params.model_type}_{model_meta.filename}"
        return model_name, model

    async def _model_generator(self, model_ids):
        for model_id in model_ids:
            yield await self._load_single_model(model_id)

    async def _load_models(self, composition_meta: ModelMetadata
                                  ) -> List[Tuple[str, Any]]:
        model_ids = composition_meta.composition_model_ids
        models = []
        async for model_name, model in self._model_generator(model_ids):
            models.append((model_name, model))
        return models

    async def _prepare_composition_params(self, composition_meta: ModelMetadata):
        return await CompositionParamsValidator(
            composition_meta).validate_params()

    async def _prepare_composition(self, composition_meta: ModelMetadata,
                                   validated_params, estimators):
        return await CompositionConstructorService().get_composition(
            composition_meta, validated_params, estimators)

    async def _validate_composition(self, composition_meta: ModelMetadata,
                                    composition, features, target):
        return await CompositionValidationService(
                composition_meta, composition
        ).validate_composition(composition_meta, features, target)

    async def predict_on_model(self, source_df_id: PydanticObjectId,
                               model_id: PydanticObjectId,
                               prediction_name: str,
                               apply_pipeline: bool = True) -> ModelMetadata:
        model_meta = await self.repository.get_model_meta(model_id)
        model = await self.repository.load_model(model_meta.id)
        features = await self._prepare_predict_data(
            model_meta, source_df_id, apply_pipeline)
        pred_df = await self._perform_prediction(model_meta, model, features)
        new_meta = await self.model_service.add_predictions(
            model_meta.id, pred_df, prediction_name)
        return new_meta

    def _check_features_equality(self, features, feature_columns):
        features_list_model = sorted(feature_columns)
        features_list_input = sorted(features.columns.tolist())
        if features_list_model != features_list_input:
            raise errors.FeaturesNotEqualError(features_list_model,
                                               features_list_input)

    async def _prepare_predict_data(self, model_meta, dataframe_id,
                                    apply_pipeline):
        """Prepare data for model predictions."""
        if apply_pipeline:
            features = await self.dataframe_service.copy_pipeline_for_prediction(
                model_meta.dataframe_id, dataframe_id)
        else:
            features, _ = await self.dataframe_service.get_feature_target_df(
                dataframe_id)

        self._check_features_equality(features, model_meta.feature_columns)
        return features[model_meta.feature_columns]

    async def _perform_prediction(self, model_meta, model, features):
        return await ModelPredictorService(model_meta, model).predict(features)



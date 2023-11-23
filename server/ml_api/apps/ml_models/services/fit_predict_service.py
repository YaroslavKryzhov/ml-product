import traceback
import functools
from typing import List, Tuple, Any

from bunnet import PydanticObjectId

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
from ml_api.apps.training_reports.services import ReportCreatorService
from ml_api.apps.dataframes.facade import DataframeServiceFacade


def handle_exceptions(method):
    @functools.wraps(method)
    def wrapper(self, model_meta, *args, **kwargs):
        try:
            return method(self, model_meta, *args, **kwargs)
        except Exception as err:
            self._process_exception(model_meta, err)
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

    def _set_status(self, model_meta: ModelMetadata,
                          status: specs.ModelStatuses):
        self.repository.set_status(model_meta.id, status)

    def _process_error(self, model_meta, err):
        self._set_status(model_meta, specs.ModelStatuses.PROBLEM)
        error_description = traceback.format_exc()
        report = ReportCreatorService().get_error_report(model_meta.task_type,
                                                         error_description)
        self.model_service.add_report(model_meta.id,
                                            model_meta.dataframe_id, report)

    def check_prediction_params(self,
            dataframe_id: PydanticObjectId, filename: str):
        self.dataframe_service.get_feature_target_column_names(dataframe_id)
        self.dataframe_service.check_prediction_filename(filename)

    @handle_exceptions
    def train_model(self, model_id: PydanticObjectId) -> ModelMetadata:
        model_meta = self.repository.get_model_meta(model_id)
        self._set_status(model_meta, specs.ModelStatuses.BUILDING)
        validated_params = self._prepare_params(model_meta)
        model = self._prepare_model(model_meta, validated_params)
        features, target = self._prepare_fit_data(model_meta)
        self._set_status(model_meta, specs.ModelStatuses.TRAINING)
        training_results = self._fit_model(model_meta, model, features, target)
        self._save_training_results(model_meta, training_results)
        self._set_status(model_meta, specs.ModelStatuses.TRAINED)
        return self.repository.get_model_meta(model_meta.id)

    def _prepare_params(self, model_meta: ModelMetadata):
        return ParamsValidationService(
            self._user_id, model_meta).validate_params()

    def _prepare_model(self, model_meta: ModelMetadata, validated_params):
        return ModelConstructorService().get_model(
            model_meta.task_type, validated_params)

    def _prepare_fit_data(self, model_meta: ModelMetadata):
        if model_meta.task_type in [specs.AvailableTaskTypes.CLASSIFICATION,
                                    specs.AvailableTaskTypes.REGRESSION]:
            return self.dataframe_service.\
                get_feature_target_df_supervised(model_meta.dataframe_id)
        else:
            return self.dataframe_service.get_feature_target_df(
                model_meta.dataframe_id)

    def _fit_model(self, model_meta: ModelMetadata, model, features,
                         target):
        return ModelTrainerService(model_meta, model
                                         ).train_model(features, target)

    def _save_training_results(self, model_meta: ModelMetadata,
                                     results: schemas.ModelTrainingResults):
        """Store trained model and related reports/predictions."""
        self.repository.save_new_model(model_meta.id, results.model)
        for report, pred_df in results.results:
            self.model_service.add_report(model_meta.id,
                                                model_meta.dataframe_id,
                                                report)
            filename = f"{model_meta.filename}_predictions" \
                       f"_{report.report_type.value}"
            self.model_service.add_predictions(model_meta.id, pred_df,
                                                     filename)

    @handle_exceptions
    def train_composition(self, composition_id: PydanticObjectId
                          ) -> ModelMetadata:
        composition_meta = self.repository.get_model_meta(composition_id)
        self._set_status(composition_meta, specs.ModelStatuses.BUILDING)
        validated_params = self._prepare_composition_params(
            composition_meta)
        estimators = self._load_models(composition_meta)
        composition = self._prepare_composition(
            composition_meta, validated_params, estimators)
        features, target = self._prepare_fit_data(composition_meta)
        self._set_status(composition_meta, specs.ModelStatuses.TRAINING)
        validation_results = self._validate_composition(
            composition_meta, composition, features, target)
        self._save_training_results(composition_meta, validation_results)
        self._set_status(composition_meta, specs.ModelStatuses.TRAINED)
        return self.repository.get_model_meta(composition_meta.id)

    def _load_single_model(self, model_id):
        model_meta = self.repository.get_model_meta(model_id)
        model = self.repository.load_model(model_id)
        model_name = f"{model_meta.model_params.model_type}_{model_meta.filename}"
        return model_name, model

    def _model_generator(self, model_ids):
        for model_id in model_ids:
            yield self._load_single_model(model_id)

    def _load_models(self, composition_meta: ModelMetadata
                                  ) -> List[Tuple[str, Any]]:
        model_ids = composition_meta.composition_model_ids
        models = []
        for model_name, model in self._model_generator(model_ids):
            models.append((model_name, model))
        return models

    def _prepare_composition_params(self, composition_meta: ModelMetadata):
        return CompositionParamsValidator(
            composition_meta).validate_params()

    def _prepare_composition(self, composition_meta: ModelMetadata,
                                   validated_params, estimators):
        return CompositionConstructorService().get_composition(
            composition_meta, validated_params, estimators)

    def _validate_composition(self, composition_meta: ModelMetadata,
                                    composition, features, target):
        return CompositionValidationService(
                composition_meta, composition
        ).validate_composition(composition_meta, features, target)

    def predict_on_model(self, source_df_id: PydanticObjectId,
                               model_id: PydanticObjectId,
                               prediction_name: str,
                               apply_pipeline: bool = True) -> ModelMetadata:
        model_meta = self.repository.get_model_meta(model_id)
        model = self.repository.load_model(model_meta.id)
        features = self._prepare_predict_data(
            model_meta, source_df_id, apply_pipeline)
        pred_df = self._perform_prediction(model_meta, model, features)
        new_meta = self.model_service.add_predictions(
            model_meta.id, pred_df, prediction_name)
        return new_meta

    def _check_features_equality(self, features, feature_columns):
        features_list_model = sorted(feature_columns)
        features_list_input = sorted(features.columns.tolist())
        if features_list_model != features_list_input:
            raise errors.FeaturesNotEqualError(features_list_model,
                                               features_list_input)

    def _prepare_predict_data(self, model_meta, dataframe_id,
                                    apply_pipeline):
        """Prepare data for model predictions."""
        if apply_pipeline:
            features = self.dataframe_service.copy_pipeline_for_prediction(
                model_meta.dataframe_id, dataframe_id)
        else:
            features, _ = self.dataframe_service.get_feature_target_df(
                dataframe_id)

        self._check_features_equality(features, model_meta.feature_columns)
        return features[model_meta.feature_columns]

    def _perform_prediction(self, model_meta, model, features):
        return ModelPredictorService(model_meta, model).predict(features)



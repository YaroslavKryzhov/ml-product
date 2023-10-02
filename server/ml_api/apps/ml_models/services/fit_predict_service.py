import traceback

from beanie import PydanticObjectId

from ml_api.apps.dataframes.services.dataframe_service import DataframeService
from ml_api.apps.dataframes.services.methods_service import DataframeMethodsService
from ml_api.apps.ml_models.services.model_construstor import \
    ModelConstructorService
from ml_api.apps.ml_models.services.model_trainer import ModelTrainerService
from ml_api.apps.ml_models.services.model_predictor import \
    ModelPredictorService
from ml_api.apps.ml_models.services.params_validator import \
    ParamsValidationService
from ml_api.apps.ml_models.services.models_service import ModelService
from ml_api.apps.ml_models.repositories.repository_manager import \
    ModelRepositoryManager
from ml_api.apps.ml_models import specs, schemas, errors
from ml_api.apps.ml_models.schemas import ModelTrainingResults
from ml_api.apps.ml_models.models import ModelMetadata
from ml_api.apps.ml_models.specs import AvailableTaskTypes as TaskTypes
from ml_api.apps.training_reports.services.report_creator import ReportCreatorService


class ModelFitPredictService:
    """
    Отвечает за обработку запросов на обучение и предсказание моделей.
    """

    def __init__(self, user_id):
        self._user_id = user_id
        self.repository = ModelRepositoryManager(self._user_id)
        self.dataframe_service = DataframeService(self._user_id)
        self.dataframe_methods_service = DataframeMethodsService(self._user_id)
        self.model_service = ModelService(self._user_id)

    async def _process_error(self, err, model_meta):
        await self.repository.set_status(model_meta.id, specs.ModelStatuses.PROBLEM)
        error_description = traceback.format_exc()
        report = ReportCreatorService().get_error_report(model_meta.task_type,
                                                         error_description)
        await self.model_service.add_report(model_meta.id,
            model_meta.dataframe_id, report)

    async def train_model(self, model_meta: ModelMetadata) -> ModelMetadata:
        model = await self._prepare_model(model_meta=model_meta)
        features, target = await self._prepare_fit_data(model_meta=model_meta)
        model_training_results = await self._fit_model(
            model_meta, model, features, target)
        new_meta = await self._save_model_training_results(model_meta,
                                                       model_training_results)
        return new_meta

    async def _prepare_model(self, model_meta: ModelMetadata):  # -> sklearn.Estimator
        model_id = model_meta.id
        await self.repository.set_status(model_id, specs.ModelStatuses.BUILDING)
        try:
            model_params_validated = await ParamsValidationService(
                self._user_id, model_meta).validate_params()
            await self.repository.set_model_params(
                model_id, model_params_validated)
            return ModelConstructorService().get_model(model_meta.task_type,
                                                       model_params_validated)
        except Exception as err:
            await self._process_error(err, model_meta)
            raise err

    async def _prepare_fit_data(self, model_meta: ModelMetadata):
        task_type = model_meta.task_type
        dataframe_id = model_meta.dataframe_id
        try:
            if task_type in [TaskTypes.CLASSIFICATION, TaskTypes.REGRESSION]:
                return await self.dataframe_service.get_feature_target_df_supervised(
                    dataframe_id=dataframe_id)
            else:
                return await self.dataframe_service.get_feature_target_df(
                    dataframe_id=dataframe_id)
        except Exception as err:
            await self._process_error(err, model_meta)
            raise err

    async def _fit_model(self, model_meta: ModelMetadata,
                         model, features, target) -> ModelTrainingResults:
        model_id = model_meta.id
        await self.repository.set_status(model_id, specs.ModelStatuses.TRAINING)
        try:
            return await ModelTrainerService(
                self._user_id, model_meta, model).train_model(features, target)
        except Exception as err:
            await self._process_error(err, model_meta)
            raise err

    async def _save_model_training_results(self, model_meta: ModelMetadata,
            model_training_results: ModelTrainingResults) -> ModelMetadata:
        model_id = model_meta.id
        source_dataframe_id = model_meta.dataframe_id

        trained_model = model_training_results.model
        try:
            await self.repository.save_new_model(model_id, trained_model)
            for report, pred_df in model_training_results.results:
                await self.model_service.add_report(model_id, source_dataframe_id,
                                       report)
                df_filename = f"{model_meta.filename}_" \
                              f"predictions_{report.report_type.value}"
                await self.model_service.add_predictions(model_id, pred_df,
                                                         df_filename)
        except Exception as err:
            await self._process_error(err, model_meta)
            raise err
        await self.repository.set_status(model_id, specs.ModelStatuses.TRAINED)
        return await self.repository.get_model_meta(model_id)

    async def predict_on_model(self, source_dataframe_id: PydanticObjectId,
                               model_id: PydanticObjectId,
                               apply_pipeline: bool = True) -> ModelMetadata:
        model_meta = await self.repository.get_model_meta(model_id)
        features = await self._prepare_predict_data(
            model_meta, source_dataframe_id, apply_pipeline)

        model = await self.repository.load_model(model_id)
        pred_df = await ModelPredictorService(
            self._user_id, model_meta, model).predict(features)
        df_filename = f"{model_meta.filename}_predictions"
        return await self.model_service.add_predictions(model_id, pred_df, df_filename)

    async def _prepare_predict_data(self, model_meta, dataframe_id, apply_pipeline):
        if apply_pipeline:
            train_df_id = model_meta.dataframe_id
            features = await self.dataframe_methods_service.copy_pipeline_for_prediction(
                train_df_id, dataframe_id)
        else:
            features, _ = await self.dataframe_service.get_feature_target_df(
                dataframe_id)
        self._check_features_equality(features, model_meta.feature_columns)
        features = features[model_meta.feature_columns]
        return features

    def _check_features_equality(self, features, feature_columns):
        features_list_model = sorted(feature_columns)
        features_list_input = sorted(features.columns.tolist())
        if features_list_model != features_list_input:
            raise errors.FeaturesNotEqualError(features_list_model,
                                               features_list_input)

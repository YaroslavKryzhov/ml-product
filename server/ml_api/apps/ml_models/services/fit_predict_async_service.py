from bunnet import PydanticObjectId

from ml_api import config
from ml_api.apps.dataframes.facade import DataframeServiceFacade
from ml_api.apps.ml_models import specs
from ml_api.apps.ml_models.model import ModelMetadata
from ml_api.apps.ml_models.repositories.repository_manager import \
    ModelRepositoryManager
from ml_api.apps.ml_models.services.fit_predict_service import \
    ModelFitPredictService
from ml_api.apps.ml_models.services.jobs_manager import ModelJobsManager
from ml_api.apps.ml_models.services.processors.composition_validator import \
    CompositionParamsValidator
from ml_api.apps.ml_models.services.processors.params_validator import \
    ParamsValidationService


class ModelFitPredictAsyncService:
    """
    Отвечает за обработку запросов на обучение и предсказание моделей.
    """
    def __init__(self, user_id):
        self._user_id = user_id
        self.repository = ModelRepositoryManager(self._user_id)
        self.fit_predict_service = ModelFitPredictService(self._user_id)
        self.dataframe_service = DataframeServiceFacade(self._user_id)

    def _set_status(self, model_meta: ModelMetadata,
                    status: specs.ModelStatuses):
        self.repository.set_status(model_meta.id, status)

    def _prepare_params(self, model_meta: ModelMetadata):
        return ParamsValidationService(
            self._user_id, model_meta).validate_params()

    def _prepare_composition_params(self, composition_meta: ModelMetadata):
        return CompositionParamsValidator(
            composition_meta).validate_params()

    def prepare_model_training(self, model_meta: ModelMetadata):
        self._set_status(model_meta, specs.ModelStatuses.WAITING)
        validated_params = self._prepare_params(model_meta)
        model_meta = self.repository.set_model_params(
            model_meta.id, validated_params)
        if config.USE_CELERY:
            return ModelJobsManager(self._user_id).process_train_model_async(
                model_meta)
        else:
            return self.fit_predict_service.train_model(model_meta.id)

    def prepare_composition_training(self, composition_meta: ModelMetadata):
        self._set_status(composition_meta, specs.ModelStatuses.WAITING)
        validated_params = self._prepare_composition_params(
            composition_meta)
        composition_meta = self.repository.set_model_params(
            composition_meta.id, validated_params)
        if config.USE_CELERY:
            return ModelJobsManager(self._user_id).process_build_composition_async(
                composition_meta)
        else:
            return self.fit_predict_service.train_composition(
                composition_meta.id)

    def prepare_prediction(self,
                           dataframe_id: PydanticObjectId,
                           model_id: PydanticObjectId,
                           prediction_name: str,
                           apply_pipeline: bool):

        self.dataframe_service.check_prediction_filename(prediction_name)
        self.dataframe_service.check_dataframe_not_prediction(dataframe_id)
        self.repository.get_model_meta(model_id)
        if config.USE_CELERY:
            return ModelJobsManager(self._user_id).predict_on_model_async(
                dataframe_id, model_id, prediction_name, apply_pipeline)
        else:
            return self.fit_predict_service.predict_on_model(
                dataframe_id, model_id, prediction_name, apply_pipeline)

import traceback

from beanie import PydanticObjectId

from ml_api.apps.ml_models.services.model_construstor import ModelConstructorService
from ml_api.apps.ml_models.services.model_trainer import ModelTrainerService
from ml_api.apps.ml_models.services.model_predictor import ModelPredictorService
from ml_api.apps.ml_models.services.params_validator import ParamsValidationService
from ml_api.apps.ml_models.services.metadata_manager import ModelMetadataManagerService
from ml_api.apps.ml_models.services.file_manager import ModelFileManagerService
from ml_api.apps.ml_models import specs
from ml_api.apps.ml_models.schemas import ModelTrainingResults
from ml_api.apps.ml_models.models import ModelMetadata
from ml_api.apps.training_reports.services.report_creator import ReportCreatorService


class ModelProcessingManagerService:
    """
    Отвечает за обработку запросов на обучение и предсказание моделей.
    """
    def __init__(self, user_id):
        self._user_id = user_id
        self.file_manager = ModelFileManagerService(self._user_id)
        self.metadata_manager = ModelMetadataManagerService(self._user_id)

    async def _set_status(self, model_id, status: specs.ModelStatuses):
        await self.metadata_manager.set_status(
            model_id, status)

    async def _process_error(self, err, model_meta):
        await self._set_status(model_meta.id, specs.ModelStatuses.PROBLEM)
        error_description = traceback.format_exc()
        report = ReportCreatorService().get_error_report(model_meta.task_type,
                                                         error_description)
        await self.metadata_manager.add_report(model_meta.id,
            model_meta.dataframe_id, report)

    async def train_model(self, model_meta: ModelMetadata):
        model = await self._prepare_model(model_meta=model_meta)
        model_training_results = await self._train_model(model_meta=model_meta, model=model)
        return await self._save_model_training_results(model_meta, model_training_results)

    async def _prepare_model(self, model_meta: ModelMetadata):  # -> sklearn.Estimator
        """
        Валидирует параметры модели и создает её экземпляр.
        """
        model_id = model_meta.id
        await self._set_status(model_id, specs.ModelStatuses.BUILDING)
        try:
            model_params_validated = await ParamsValidationService(
                self._user_id, model_meta).validate_params()

            await self.metadata_manager.set_model_params(
                model_id, model_params_validated)

            return ModelConstructorService().get_model(model_meta.task_type,
                                                       model_params_validated)
        except Exception as err:
            await self._process_error(err, model_meta)
            raise err

    async def _train_model(self, model_meta: ModelMetadata, model) -> ModelTrainingResults:
        """
        Обучает предоставленную модель на данных из датафрейма.
        """
        model_id = model_meta.id
        await self.metadata_manager.set_status(model_id, specs.ModelStatuses.TRAINING)
        try:
            return await ModelTrainerService(self._user_id,
                model_meta, model).train_model()
        except Exception as err:
            await self._process_error(err, model_meta)
            raise err

    async def _save_model_training_results(self, model_meta: ModelMetadata,
            model_training_results: ModelTrainingResults):
        model_id = model_meta.id
        dataframe_id = model_meta.dataframe_id
        try:
            await self.file_manager.save_model(model_id, model_training_results.model)
            for report, pred_df in model_training_results.results:
                await self.metadata_manager.add_report(model_id, dataframe_id,
                                                       report)
                df_filename = f"{model_meta.filename}_" \
                                  f"predictions_{report.report_type.value}"
                await self.metadata_manager.add_predictions(model_id, pred_df,
                                                            dataframe_id,
                                                            df_filename)
        except Exception as err:
            await self._process_error(err, model_meta)
            raise err

        await self.metadata_manager.set_status(model_id, specs.ModelStatuses.TRAINED)

        return await self.metadata_manager.get_model_meta(model_id)

    async def predict_on_model(self, dataframe_id: PydanticObjectId,
                         model_id: PydanticObjectId,
                         apply_pipeline: bool = True):
        model_meta = await self.metadata_manager.get_model_meta(model_id)
        pred_df = await ModelPredictorService(self._user_id, model_meta).predict(
            dataframe_id, apply_pipeline)
        df_filename = f"{model_meta.filename}_predictions"
        await self.metadata_manager.add_predictions(model_id, pred_df,
                                                    dataframe_id,
                                                    df_filename)

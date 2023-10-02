from beanie import PydanticObjectId
from pandas import DataFrame

from ml_api.apps.ml_models.repositories.repository_manager import ModelRepositoryManager
from ml_api.apps.ml_models import specs, schemas, errors
from ml_api.apps.ml_models.models import ModelMetadata
from ml_api.apps.dataframes.services.dataframe_service import DataframeService
from ml_api.apps.training_reports.repository import TrainingReportCRUD
from ml_api.apps.training_reports.models import Report


class ModelService:
    """
    Отвечает за обработку запросов на обучение и предсказание моделей.
    """
    def __init__(self, user_id):
        self._user_id = user_id
        self.repository = ModelRepositoryManager(self._user_id)
        self.dataframe_service = DataframeService(self._user_id)
        self.report_crud = TrainingReportCRUD(self._user_id)

    async def create_model(self,
                           model_name: str,
                           dataframe_id: PydanticObjectId,
                           task_type: specs.AvailableTaskTypes,
                           model_params: schemas.ModelParams,
                           params_type: specs.AvailableParamsTypes,
                           test_size: float,
                           stratify: bool) -> ModelMetadata:
        feature_columns, target_column = await self.dataframe_service.get_feature_target_column_names(
            dataframe_id=dataframe_id)

        if (task_type == specs.AvailableTaskTypes.CLASSIFICATION or
                task_type == specs.AvailableTaskTypes.REGRESSION):
            if target_column is None:
                raise errors.TargetNotFoundSupervisedLearningError(
                    dataframe_id=dataframe_id)

        model_meta = await self.repository.create_model(
            model_name=model_name,
            dataframe_id=dataframe_id,
            task_type=task_type,
            model_params=model_params,
            params_type=params_type,
            feature_columns=feature_columns,
            target_column=target_column,
            test_size=test_size,
            stratify=stratify)
        return model_meta

    async def add_report(self, model_id: PydanticObjectId,
                         dataframe_id: PydanticObjectId,
                         report: Report) -> ModelMetadata:
        report.user_id = self._user_id
        report.model_id = model_id
        report.dataframe_id = dataframe_id
        report = await self.report_crud.save(report)
        return await self.repository.add_report(model_id, report.id)

    async def add_predictions(self, model_id: PydanticObjectId,
                              pred_df: DataFrame,
                              df_filename: str) -> ModelMetadata:
        pred_df_info = await self.dataframe_service.save_predictions_dataframe(
            df_filename, pred_df)
        return await self.repository.add_predictions(model_id, pred_df_info.id)



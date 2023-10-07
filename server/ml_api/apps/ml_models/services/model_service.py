from beanie import PydanticObjectId
from pandas import DataFrame


from ml_api.apps.ml_models import specs, schemas, errors
from ml_api.apps.ml_models.models import ModelMetadata
from ml_api.apps.ml_models.repositories.repository_manager import ModelRepositoryManager
from ml_api.apps.training_reports.models import Report
from ml_api.apps.training_reports.repository import TrainingReportCRUD


class ModelService:
    """
    Отвечает за обработку запросов на обучение и предсказание моделей.
    """
    def __init__(self, user_id):
        self._user_id = user_id
        self.repository = ModelRepositoryManager(self._user_id)
        self.report_crud = TrainingReportCRUD(self._user_id)

    # 1: CREATE OPERATIONS ----------------------------------------------------
    async def create_model(self,
                           model_name: str,
                           dataframe_id: PydanticObjectId,
                           task_type: specs.AvailableTaskTypes,
                           model_params: schemas.ModelParams,
                           params_type: specs.AvailableParamsTypes,
                           test_size: float,
                           stratify: bool) -> ModelMetadata:
        from ml_api.apps.dataframes.services.for_model_service import \
            DataframeForModelService
        feature_columns, target_column = await DataframeForModelService(
            self._user_id).get_feature_target_column_names(
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
        from ml_api.apps.dataframes.services.for_model_service import \
            DataframeForModelService
        pred_df_info = await DataframeForModelService(
            self._user_id).save_predictions_dataframe(
            df_filename, pred_df)
        return await self.repository.add_prediction(model_id, pred_df_info.id)

    # 2: GET OPERATIONS -------------------------------------------------------
    async def download_model(self, model_id):
        return await self.repository.download_model(model_id)

    async def get_model_meta(self, model_id):
        return await self.repository.get_model_meta(model_id)

    async def get_all_models_meta(self):
        return await self.repository.get_all_models_meta()

    async def get_all_models_meta_by_dataframe(self, dataframe_id):
        return await self.repository.get_all_models_meta_by_dataframe(
            dataframe_id)

    # 3: UPDATE OPERATIONS ----------------------------------------------------
    async def set_filename(self, model_id, new_model_name):
        return await self.repository.set_filename(model_id, new_model_name)

    # 4: DELETE OPERATIONS ----------------------------------------------------
    async def delete_model(self, model_id: PydanticObjectId) -> ModelMetadata:
        from ml_api.apps.dataframes.services.for_model_service import \
            DataframeForModelService
        dataframe_service = DataframeForModelService(self._user_id)
        model_meta = await self.repository.get_model_meta(model_id)
        for prediction_id in model_meta.model_prediction_ids:
            await dataframe_service.delete_prediction(prediction_id)
        for report_id in model_meta.metrics_report_ids:
            await self.report_crud.delete(report_id)
        model_meta = await self.repository.delete_model(model_id)
        return model_meta

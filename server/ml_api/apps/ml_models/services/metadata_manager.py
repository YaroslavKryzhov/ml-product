from typing import List

from beanie import PydanticObjectId

from ml_api.apps.dataframes.services.dataframe_manager import \
    DataframeManagerService
from ml_api.apps.ml_models import specs, schemas
from ml_api.apps.ml_models.models import ModelMetadata
from ml_api.apps.ml_models.repository import ModelInfoCRUD, ModelFileCRUD
from ml_api.apps.ml_models import errors


class ModelMetadataManagerService:
    """
    Работает с данными в MongoDB, обеспечивает доступ и управление метадатой.
    """

    def __init__(self, user_id):
        self._user_id = user_id
        self.info_repository = ModelInfoCRUD(self._user_id)
        self.file_repository = ModelFileCRUD(self._user_id)
        self.dataframe_manager = DataframeManagerService(self._user_id)

    async def get_model_meta(self, model_id: PydanticObjectId
                             ) -> ModelMetadata:
        return await self.info_repository.get(model_id)

    async def get_all_models_meta(self) -> List[ModelMetadata]:
        return await self.info_repository.get_all()

    async def get_all_models_meta_by_dataframe(self,
            dataframe_id: PydanticObjectId) -> List[ModelMetadata]:
        return await self.info_repository.get_by_dataframe_id(dataframe_id)

    def _gather_new_filename(self, filename: str):
        """
        Собирает новое имя файла модели, включая расширение.
        """
        if not filename.endswith('.pickle'):
            filename += '.pickle'
        return filename

    async def create_model(self,
                           model_name: str,
                           dataframe_id: PydanticObjectId,
                           task_type: specs.AvailableTaskTypes,
                           model_params: schemas.ModelParams,
                           params_type: specs.AvailableParamsTypes,
                           test_size: float) -> ModelMetadata:
        feature_columns, target_column = self.dataframe_manager.get_feature_target_column_names(
            dataframe_id=dataframe_id)

        if (task_type == specs.AvailableTaskTypes.CLASSIFICATION or
                task_type == specs.AvailableTaskTypes.REGRESSION):
            if target_column is None:
                raise errors.TargetNotFoundSupervisedLearningError(
                    dataframe_id=dataframe_id)

        model_meta = await self.info_repository.create(
            filename=self._gather_new_filename(model_name),
            dataframe_id=dataframe_id,
            task_type=task_type,
            model_params=model_params,
            params_type=params_type,
            feature_columns=feature_columns,
            target_column=target_column,
            test_size=test_size)
        return model_meta

    async def set_filename(self, model_id: PydanticObjectId,
                           new_filename: str) -> ModelMetadata:
        query = {"$set": {
            ModelMetadata.filename:
            self._gather_new_filename(new_filename)}}
        return await self.info_repository.update(model_id, query)

    async def set_status(self, model_id: PydanticObjectId,
                         new_status: specs.ModelStatuses) -> ModelMetadata:
        query = {"$set": {ModelMetadata.status: new_status}}
        return await self.info_repository.update(model_id, query)

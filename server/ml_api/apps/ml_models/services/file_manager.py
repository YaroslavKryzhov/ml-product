from typing import List

from beanie import PydanticObjectId
from fastapi.responses import FileResponse

from ml_api.apps.dataframes.services.dataframe_manager import \
    DataframeManagerService
from ml_api.apps.ml_models import specs, schemas
from ml_api.apps.ml_models.models import ModelMetadata
from ml_api.apps.ml_models.repository import ModelInfoCRUD, ModelFileCRUD
from ml_api.apps.ml_models import errors


class ModelFileManagerService:
    """
    Работает с файлами ОС и отвечает за синхронизацию файловой системы с данными в MongoDB
    при добавлении/удалении файлов. Также отвечает за доступ к файлам.
    """
    def __init__(self, user_id):
        self._user_id = user_id
        self.info_repository = ModelInfoCRUD(self._user_id)
        self.file_repository = ModelFileCRUD(self._user_id)
        self.dataframe_manager = DataframeManagerService(self._user_id)

    # 1: FILE MANAGEMENT OPERATIONS -------------------------------------------
    async def download_file(self, model_id: PydanticObjectId,
                            model_format: specs.ModelFormats) -> FileResponse:
        # TODO: add onnx format conversion
        # feature_example = features[:1].astype(np.float32).values,
        # onx = to_onnx(model, feature_example)
        model_meta = await self.info_repository.get(model_id)
        response = self.file_repository.download_model(
            file_id=model_id, filename=model_meta.filename)
        return response

    async def save_model(self, model_id: PydanticObjectId, model
                         ) -> ModelMetadata:
        model_meta = await self.info_repository.get(model_id)
        if model_meta.status != specs.ModelStatuses.TRAINED:
            raise errors.ModelNotTrainedError(model_id=model_id)
        self.file_repository.save_model(model_id, model)
        return model_meta

    async def load_model_from_file(self, dataframe_id: PydanticObjectId
                                ) -> pd.DataFrame:
        return self.file_repository.read_csv(dataframe_id)

    async def delete_file(self, model_id: PydanticObjectId) -> ModelMetadata:
        model_meta = await self.info_repository.delete(model_id)
        self.file_repository.delete(model_id)
        return model_meta

from typing import List

from beanie import PydanticObjectId
from fastapi.responses import FileResponse

from ml_api.apps.ml_models.models import ModelMetadata
from ml_api.apps.ml_models.repository import ModelInfoCRUD, ModelFileCRUD


class ModelFileManagerService:
    """
    Работает с файлами ОС и отвечает за синхронизацию файловой системы с данными в MongoDB
    при добавлении/удалении файлов. Также отвечает за доступ к файлам.
    """
    def __init__(self, user_id):
        self._user_id = user_id
        self.info_repository = ModelInfoCRUD(self._user_id)
        self.file_repository = ModelFileCRUD(self._user_id)

    # 1: FILE MANAGEMENT OPERATIONS -------------------------------------------
    async def download_file(self, model_id: PydanticObjectId) -> FileResponse:
        # add onnx format conversion if needed
        # feature_example = features[:1].astype(np.float32).values,
        # onx = to_onnx(model, feature_example)
        model_meta = await self.info_repository.get(model_id)
        response = self.file_repository.download_model(
            file_id=model_id, filename=model_meta.filename)
        return response

    async def save_model(self, model_id: PydanticObjectId, model
                         ) -> ModelMetadata:
        self.file_repository.save_model(model_id, model)

    async def load_model_from_file(self, model_id: PydanticObjectId):
        return self.file_repository.read_model(model_id)

    async def delete_file(self, model_id: PydanticObjectId) -> ModelMetadata:
        # TODO: rewrite model deletion to cascade
        model_meta = await self.info_repository.delete(model_id)
        self.file_repository.delete_model(model_id)
        return model_meta

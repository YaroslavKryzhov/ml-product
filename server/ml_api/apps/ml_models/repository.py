from typing import List, Dict
import pickle

from beanie import PydanticObjectId
from pymongo.errors import DuplicateKeyError
from fastapi.responses import FileResponse

from ml_api.common.file_manager.base import FileCRUD
from ml_api.apps.ml_models.models import ModelMetadata
from ml_api.apps.ml_models.schemas import ModelParams
from ml_api.apps.ml_models.specs import AvailableTaskTypes, \
    AvailableParamsTypes, AvailableModelTypes
from ml_api.apps.ml_models.errors import ModelNotFoundError, \
    FilenameExistsUserError, ObjectFileNotFoundError


class ModelInfoCRUD:
    def __init__(self, user_id: PydanticObjectId):
        self.user_id = user_id

    async def get(self, model_id: PydanticObjectId) -> ModelMetadata:
        model_meta = await ModelMetadata.get(model_id)
        if model_meta is None:
            raise ModelNotFoundError(model_id)
        return model_meta

    async def get_all(self) -> List[ModelMetadata]:
        model_metas = await ModelMetadata.find(
            ModelMetadata.user_id == self.user_id).to_list()
        return model_metas

    async def get_by_dataframe_id(self, dataframe_id: PydanticObjectId
                                  ) -> List[ModelMetadata]:
        models = await ModelMetadata.find(
            (ModelMetadata.user_id == self.user_id) &
            (ModelMetadata.dataframe_id == dataframe_id)
        ).to_list()
        return models

    async def create(self,
                     filename: str,
                     dataframe_id: PydanticObjectId,
                     task_type: AvailableTaskTypes,
                     model_params: ModelParams,
                     params_type: AvailableParamsTypes,
                     feature_columns: List[str],
                     target_column: str,
                     test_size: float) -> ModelMetadata:
        new_obj = ModelMetadata(filename=filename,
                                user_id=self.user_id,
                                dataframe_id=dataframe_id,
                                task_type=task_type,
                                model_params=model_params,
                                params_type=params_type,
                                feature_columns=feature_columns,
                                target_column=target_column,
                                test_size=test_size)
        try:
            await new_obj.insert()
        except DuplicateKeyError:
            raise FilenameExistsUserError(filename)
        return new_obj

    async def update(self, model_id: PydanticObjectId, query: Dict
                     ) -> ModelMetadata:
        model_meta = await ModelMetadata.get(model_id)
        if model_meta is None:
            raise ModelNotFoundError(model_id)
        return await model_meta.update(query)

    async def delete(self, model_id: PydanticObjectId) -> ModelMetadata:
        model_meta = await ModelMetadata.get(model_id)
        if model_meta is None:
            raise ModelNotFoundError(model_id)
        return await model_meta.delete()


class ModelFileCRUD(FileCRUD):

    def read_model(self, file_id: PydanticObjectId):
        """Read model file"""
        model_path = self._get_path(file_id)
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
        except FileNotFoundError:
            raise ObjectFileNotFoundError(file_id)
        return model

    def download_model(self, file_id: PydanticObjectId,
                       filename: str) -> FileResponse:
        file_response = self.download(file_id=file_id, filename=filename)
        return file_response

    def save_model(self, file_id: PydanticObjectId, model):
        """Save model file"""
        model_path = self._get_path(file_id)
        with open(model_path, "wb") as f:
            pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)


# class ModelFileCRUD(FileCRUD):
#
#     def read_onnx(self, model_uuid: UUID):
#         model_path = self._get_path(model_uuid)
#         try:
#             model = InferenceSession(model_path)
#         except FileNotFoundError:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"Saved model with id {model_uuid} not found."
#             )
#         return model
#
#     def download_model(self, model_uuid: UUID, filename: str) -> FileResponse:
#         file_response = self.download(file_uuid=model_uuid, filename=filename)
#         return file_response
#
#     def save_onnx(self, model_uuid: UUID, model):
#         """Save model in the ONNX format"""
#         model_path = self._get_path(model_uuid)
#         with open(model_path, "wb") as f:
#             f.write(model.SerializeToString())
#
#     """
#     Some pickled models (like catboost) don't work properly after saving and load.
#     """
#     def read_pickle(self, model_uuid: UUID):
#         model_path = self._get_path(model_uuid)
#         try:
#             with open(model_path, 'rb') as f:
#                 model = pickle.load(f)
#         except FileNotFoundError:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"Saved model with id {model_uuid} not found."
#             )
#         return model
#
#     def save_pickle(self, model_uuid: UUID, model):
#         """Save model in the pickle format"""
#         model_path = self._get_path(model_uuid)
#         with open(model_path, "wb") as f:
#             pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)

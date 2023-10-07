from pathlib import Path
import joblib
from beanie import PydanticObjectId
from fastapi.responses import FileResponse

from ml_api.apps.ml_models import errors
from ml_api.common.file_manager.base import FileCRUD
from ml_api.config import ROOT_DIR


class ModelFileCRUD(FileCRUD):
    def __init__(self, user_id):
        self.user_id = user_id

    def _get_joblib_path(self, file_id: PydanticObjectId):
        user_path = Path(ROOT_DIR) / str(self.user_id) / "models"
        user_path.mkdir(parents=True, exist_ok=True)
        return user_path / f"{file_id}.joblib"

    def download_model(self, file_id: PydanticObjectId, filename: str
                     ) -> FileResponse:
        joblib_path = self._get_joblib_path(file_id)
        if not filename.endswith('.joblib'):
            filename += '.joblib'
        file_response = self._download(path=joblib_path, filename=filename)
        return file_response

    def read_model(self, file_id: PydanticObjectId):  # -> Estimator object
        """Read model file"""
        joblib_path = self._get_joblib_path(file_id)
        try:
            model = joblib.load(joblib_path)
        except FileNotFoundError:
            raise errors.ModelFileNotFoundError(file_id)
        return model

    def save_model(self, file_id: PydanticObjectId, model):
        """Save model file"""
        joblib_path = self._get_joblib_path(file_id)
        joblib.dump(model, joblib_path)

    def delete_model(self, file_id: PydanticObjectId):
        """Delete model file"""
        joblib_path = self._get_joblib_path(file_id)
        self._delete(joblib_path)


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
#     def download_model(self, model_uuid: UUID, filename: str
#     ) -> FileResponse:
#         file_response = self.download(file_uuid=model_uuid,
#         filename=filename)
#         return file_response
#
#     def save_onnx(self, model_uuid: UUID, model):
#         """Save model in the ONNX format"""
#         model_path = self._get_path(model_uuid)
#         with open(model_path, "wb") as f:
#             f.write(model.SerializeToString())
#
#     """
#     Some pickled models (like catboost) don't work properly after saving
#     and load.
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

from typing import List, Optional

from bunnet import PydanticObjectId
from fastapi.responses import FileResponse
from pymongo.errors import DuplicateKeyError

from ml_api.apps.ml_models import specs, schemas, errors
from ml_api.apps.ml_models.model import ModelMetadata
from ml_api.apps.ml_models.repositories.meta_repository import ModelMetaCRUD
from ml_api.apps.ml_models.repositories.file_repository import ModelFileCRUD


class ModelRepositoryManager:
    """
    Работает с файлами ОС и отвечает за синхронизацию файловой системы
    с данными в MongoDB
    при добавлении/удалении файлов. Также отвечает за доступ к файлам.
    """

    def __init__(self, user_id):
        self._user_id = user_id
        self.meta_repository = ModelMetaCRUD(self._user_id)
        self.file_repository = ModelFileCRUD(self._user_id)

    # 1: FILE MANAGEMENT OPERATIONS -------------------------------------------

    def create_model(self,
                     model_name: str,
                     dataframe_id: PydanticObjectId,
                     is_composition: bool,
                     task_type: specs.AvailableTaskTypes,
                     model_params: schemas.ModelParams,
                     params_type: specs.AvailableParamsTypes,
                     feature_columns: List[str],
                     target_column: str,
                     test_size: float,
                     stratify: bool,
                     composition_model_ids: Optional[
                         List[PydanticObjectId]] = None
                     ) -> ModelMetadata:
        model_meta = self.meta_repository.create(
            filename=model_name,
            dataframe_id=dataframe_id,
            is_composition=is_composition,
            task_type=task_type,
            model_params=model_params,
            params_type=params_type,
            feature_columns=feature_columns,
            target_column=target_column,
            test_size=test_size,
            stratify=stratify,
            composition_model_ids=composition_model_ids
        )
        return model_meta

    def save_new_model(self, model_id: PydanticObjectId, model
                       ) -> ModelMetadata:
        self.file_repository.save_model(model_id, model)

    def download_model(self, model_id: PydanticObjectId) -> FileResponse:
        # add onnx format conversion if needed
        # feature_example = features[:1].astype(np.float32).values,
        # onx = to_onnx(model, feature_example)
        model_meta = self.meta_repository.get(model_id)
        response = self.file_repository.download_model(
            file_id=model_id, filename=model_meta.filename)
        return response

    def load_model(self, model_id: PydanticObjectId):
        return self.file_repository.read_model(model_id)

    def delete_model(self, model_id: PydanticObjectId) -> ModelMetadata:
        model_meta = self.meta_repository.delete(model_id)
        if model_meta.status == specs.ModelStatuses.TRAINED:
            self.file_repository.delete_model(model_id)
        return model_meta

    # 2: GET METADATA OPERATIONS ----------------------------------------------
    def get_by_filename(self, filename: str) -> ModelMetadata:
        return self.meta_repository.get_by_filename(filename)

    def get_model_meta(self, model_id: PydanticObjectId
                       ) -> ModelMetadata:
        return self.meta_repository.get(model_id)

    def get_all_models_meta(self) -> List[ModelMetadata]:
        return self.meta_repository.get_all()

    def get_all_models_meta_by_dataframe(self,
                                         dataframe_id: PydanticObjectId) -> \
    List[ModelMetadata]:
        return self.meta_repository.get_by_dataframe_id(dataframe_id)

    def get_filename(self, model_id: PydanticObjectId
                     ) -> str:
        model_meta = self.get_model_meta(model_id)
        return model_meta.filename

    def get_dataframe_id(self, model_id: PydanticObjectId
                         ) -> PydanticObjectId:
        model_meta = self.get_model_meta(model_id)
        return model_meta.dataframe_id

    def get_task_type(self, model_id: PydanticObjectId
                      ) -> specs.AvailableTaskTypes:
        model_meta = self.get_model_meta(model_id)
        return model_meta.task_type

    def get_model_params(self, model_id: PydanticObjectId
                         ) -> schemas.ModelParams:
        model_meta = self.get_model_meta(model_id)
        return model_meta.model_params

    def get_params_type(self, model_id: PydanticObjectId
                        ) -> specs.AvailableParamsTypes:
        model_meta = self.get_model_meta(model_id)
        return model_meta.params_type

    def get_feature_columns(self, model_id: PydanticObjectId
                            ) -> Optional[List[str]]:
        model_meta = self.get_model_meta(model_id)
        return model_meta.feature_columns

    def get_target_column(self, model_id: PydanticObjectId
                          ) -> Optional[str]:
        model_meta = self.get_model_meta(model_id)
        return model_meta.target_column

    def get_status(self, model_id: PydanticObjectId
                   ) -> specs.ModelStatuses:
        model_meta = self.get_model_meta(model_id)
        return model_meta.status

    def get_metrics_report_ids(self, model_id: PydanticObjectId
                               ) -> List[PydanticObjectId]:
        model_meta = self.get_model_meta(model_id)
        return model_meta.metrics_report_ids

    def get_model_prediction_ids(self, model_id: PydanticObjectId
                                 ) -> List[PydanticObjectId]:
        model_meta = self.get_model_meta(model_id)
        return model_meta.model_prediction_ids

    # 3: SET METADATA OPERATIONS ----------------------------------------------

    def set_filename(self, model_id: PydanticObjectId,
                     new_filename: str) -> ModelMetadata:
        query = {"$set": {ModelMetadata.filename: new_filename}}
        return self.meta_repository.update(model_id, query)

    def set_status(self, model_id: PydanticObjectId,
                   new_status: specs.ModelStatuses) -> ModelMetadata:
        query = {"$set": {ModelMetadata.status: new_status}}
        return self.meta_repository.update(model_id, query)

    def set_model_params(self, model_id: PydanticObjectId,
                         new_model_params: schemas.ModelParams
                         ) -> ModelMetadata:
        query = {"$set": {ModelMetadata.model_params: new_model_params}}
        return self.meta_repository.update(model_id, query)

    def add_report(self, model_id: PydanticObjectId,
                   report_id: PydanticObjectId) -> ModelMetadata:
        query = {"$push": {ModelMetadata.metrics_report_ids: report_id}}
        return self.meta_repository.update(model_id, query)

    def add_prediction(self, model_id: PydanticObjectId,
                       prediction_id: PydanticObjectId) -> ModelMetadata:
        query = {"$push": {ModelMetadata.model_prediction_ids: prediction_id}}
        return self.meta_repository.update(model_id, query)

    def remove_prediction(self, model_id: PydanticObjectId,
                          prediction_id: PydanticObjectId
                          ) -> ModelMetadata:
        query = {"$pull": {ModelMetadata.model_prediction_ids: prediction_id}}
        return self.meta_repository.update(model_id, query)

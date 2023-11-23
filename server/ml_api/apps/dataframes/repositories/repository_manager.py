from typing import List, Optional

from bunnet import PydanticObjectId
from fastapi.responses import FileResponse
import pandas as pd

from ml_api.apps.dataframes.repositories.meta_repository import DataFrameMetaCRUD
from ml_api.apps.dataframes.repositories.file_repository import DataFrameFileCRUD
from ml_api.apps.dataframes.model import DataFrameMetadata
from ml_api.apps.dataframes import schemas, errors


class DataframeRepositoryManager:
    """
    Управляет операциями с хранилищами данных, выполняя синхронизацию файловой
    системы с MongoDB обеспечивая доступ к файлам, их загрузку, удаление и
    обновление метаданных, а также управление атрибутами метаданных.
    """

    def __init__(self, user_id):
        self._user_id = user_id
        self.meta_repository = DataFrameMetaCRUD(self._user_id)
        self.file_repository = DataFrameFileCRUD(self._user_id)

    # 1: FILE MANAGEMENT OPERATIONS -------------------------------------------
    def upload_dataframe(self, file, filename: str) -> DataFrameMetadata:
        dataframe_meta = self.meta_repository.create(filename=filename)
        self.file_repository.upload_csv(file_id=dataframe_meta.id, file=file)
        return dataframe_meta

    def save_as_new_dataframe(self, df: pd.DataFrame,
                                    dataframe_meta: DataFrameMetadata
                                    ) -> DataFrameMetadata:

        new_dataframe_meta = self.meta_repository.create(
            parent_id=dataframe_meta.parent_id,
            filename=dataframe_meta.filename,
            is_prediction=dataframe_meta.is_prediction,
            feature_columns_types=dataframe_meta.feature_columns_types,
            target_feature=dataframe_meta.target_feature,
            pipeline=dataframe_meta.pipeline,
            feature_importance_report=dataframe_meta.feature_importance_report
        )
        self.file_repository.save_csv(new_dataframe_meta.id, df)
        return new_dataframe_meta

    def save_prediction_dataframe(self, df, filename: str) -> DataFrameMetadata:
        dataframe_meta = self.meta_repository.create(filename=filename,
                                                           is_prediction=True)
        self.file_repository.save_csv(dataframe_meta.id, df)
        return dataframe_meta

    def download_dataframe(self, dataframe_id: PydanticObjectId
                                 ) -> FileResponse:
        filename = self.get_filename(dataframe_id)
        response = self.file_repository.download_csv(
            file_id=dataframe_id, filename=filename)
        return response

    def read_pandas_dataframe(self, dataframe_id: PydanticObjectId
                                    ) -> pd.DataFrame:
        self.get_dataframe_meta(dataframe_id)
        return self.file_repository.read_csv(dataframe_id)

    def save_pandas_dataframe(self, dataframe_id: PydanticObjectId,
                                    df: pd.DataFrame) -> None:
        self.get_dataframe_meta(dataframe_id)
        self.file_repository.save_csv(dataframe_id, df)

    def delete_dataframe(self,
                               dataframe_id: PydanticObjectId) -> DataFrameMetadata:
        dataframe_meta = self.meta_repository.delete(dataframe_id)
        self.file_repository.delete_csv(dataframe_id)
        return dataframe_meta

    # 2: GET METADATA OPERATIONS ----------------------------------------------
    def get_by_filename(self, filename: str) -> DataFrameMetadata:
        return self.meta_repository.get_by_filename(filename)

    def get_dataframe_meta(self, dataframe_id: PydanticObjectId
                                 ) -> DataFrameMetadata:
        return self.meta_repository.get(dataframe_id)

    def get_active_dataframes_meta(self) -> List[DataFrameMetadata]:
        return self.meta_repository.get_active()

    def get_dataframe_metas_by_parent_id(
            self, parent_id: PydanticObjectId) -> List[DataFrameMetadata]:
        return self.meta_repository.get_by_parent_id(parent_id)

    def get_parent_id(self, dataframe_id: PydanticObjectId
                            ) -> Optional[PydanticObjectId]:
        dataframe_meta = self.get_dataframe_meta(dataframe_id)
        return dataframe_meta.parent_id

    def get_is_prediction(self, dataframe_id: PydanticObjectId
                                ) -> Optional[PydanticObjectId]:
        dataframe_meta = self.get_dataframe_meta(dataframe_id)
        return dataframe_meta.is_prediction

    def get_filename(self, dataframe_id: PydanticObjectId
                           ) -> str:
        dataframe_meta = self.get_dataframe_meta(dataframe_id)
        return dataframe_meta.filename

    def get_feature_column_types(self, dataframe_id: PydanticObjectId
                                       ) -> Optional[schemas.ColumnTypes]:
        dataframe_meta = self.get_dataframe_meta(dataframe_id)
        return dataframe_meta.feature_columns_types

    def get_target_feature(self, dataframe_id: PydanticObjectId
                                 ) -> Optional[str]:
        dataframe_meta = self.get_dataframe_meta(dataframe_id)
        return dataframe_meta.target_feature

    def get_pipeline(self, dataframe_id: PydanticObjectId
                           ) -> Optional[List[schemas.ApplyMethodParams]]:
        dataframe_meta = self.get_dataframe_meta(dataframe_id)
        return dataframe_meta.pipeline

    def get_feature_importance_report(
            self, dataframe_id: PydanticObjectId
    ) -> Optional[schemas.FeatureSelectionSummary]:
        dataframe_meta = self.get_dataframe_meta(dataframe_id)
        return dataframe_meta.feature_importance_report

    # 3: SET METADATA OPERATIONS ----------------------------------------------

    def set_parent_id(self, dataframe_id,
                            new_parent_id: Optional[PydanticObjectId]
                            ) -> DataFrameMetadata:
        query = {"$set": {DataFrameMetadata.parent_id: new_parent_id}}
        return self.meta_repository.update(dataframe_id, query)

    def set_filename(self, dataframe_id: PydanticObjectId,
                           new_filename: str) -> DataFrameMetadata:
        query = {"$set": {DataFrameMetadata.filename: new_filename}}
        return self.meta_repository.update(dataframe_id, query)

    def set_is_prediction(self, dataframe_id, value: bool
                                ) -> DataFrameMetadata:
        query = {"$set": {DataFrameMetadata.is_prediction: value}}
        return self.meta_repository.update(dataframe_id, query)

    def set_feature_column_types(
            self,
            dataframe_id: PydanticObjectId,
            column_types: schemas.ColumnTypes) -> DataFrameMetadata:
        query = {
            "$set": {DataFrameMetadata.feature_columns_types: column_types}}
        return self.meta_repository.update(dataframe_id, query)

    def set_target_feature(self, dataframe_id: PydanticObjectId,
                                 target_feature: str) -> DataFrameMetadata:
        query = {"$set": {DataFrameMetadata.target_feature: target_feature}}
        return self.meta_repository.update(dataframe_id, query)

    def set_pipeline(self, dataframe_id: PydanticObjectId,
                           pipeline: List[schemas.ApplyMethodParams]
                           ) -> DataFrameMetadata:
        query = {"$set": {DataFrameMetadata.pipeline: pipeline}}
        return self.meta_repository.update(dataframe_id, query)

    def set_feature_importance_report(
            self,
            dataframe_id: PydanticObjectId,
            feature_importances: schemas.FeatureSelectionSummary
    ) -> DataFrameMetadata:
        query = {"$set": {
            DataFrameMetadata.feature_importance_report: feature_importances}}
        return self.meta_repository.update(dataframe_id, query)

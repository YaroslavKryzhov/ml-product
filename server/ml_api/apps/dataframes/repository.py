import tempfile
from pathlib import Path
from typing import List
from typing import Dict

import pandas as pd
from fastapi.responses import FileResponse
from beanie import PydanticObjectId
from pymongo.errors import DuplicateKeyError

from ml_api.common.file_manager.base import FileCRUD
from ml_api.config import ROOT_DIR
from ml_api.apps.dataframes.models import DataFrameMetadata, ColumnTypes
from ml_api.apps.dataframes.errors import FilenameExistsUserError, \
    DataFrameNotFoundError, ObjectFileNotFoundError


class DataFrameInfoCRUD:
    def __init__(self, user_id: PydanticObjectId):
        self.user_id = user_id

    async def get(self, dataframe_id: PydanticObjectId) -> DataFrameMetadata:
        dataframe_meta = await DataFrameMetadata.get(dataframe_id)
        if dataframe_meta is None:
            raise DataFrameNotFoundError(dataframe_id)
        return dataframe_meta

    async def get_all(self) -> List[DataFrameMetadata]:
        dataframe_metas = await DataFrameMetadata.find(
            DataFrameMetadata.user_id == self.user_id).find(
            DataFrameMetadata.is_prediction == False).to_list()
        return dataframe_metas

    async def create_new(self, filename: str) -> DataFrameMetadata:
        new_obj = DataFrameMetadata(filename=filename, user_id=self.user_id)
        try:
            await new_obj.insert()
        except DuplicateKeyError:
            raise FilenameExistsUserError(filename)
        return new_obj

    async def create_from_meta(self, dataframe_meta: DataFrameMetadata
                               ) -> DataFrameMetadata:
        new_dataframe_meta = DataFrameMetadata(
            parent_id=dataframe_meta.parent_id,
            filename=dataframe_meta.filename,
            user_id=dataframe_meta.user_id,
            is_prediction=dataframe_meta.is_prediction,
            feature_columns_types=dataframe_meta.feature_columns_types,
            target_feature=dataframe_meta.target_feature,
            pipeline=dataframe_meta.pipeline
        )
        try:
            await new_dataframe_meta.insert()
        except DuplicateKeyError:
            raise FilenameExistsUserError(new_dataframe_meta.filename)
        return new_dataframe_meta

    async def update(self, dataframe_id: PydanticObjectId, query: Dict
                     ) -> DataFrameMetadata:
        dataframe_meta = await DataFrameMetadata.get(dataframe_id)
        if not dataframe_meta:
            raise DataFrameNotFoundError(dataframe_id)
        await dataframe_meta.update(query)
        dataframe_meta_updated = await DataFrameMetadata.get(dataframe_id)
        return dataframe_meta_updated

    async def delete(self, dataframe_id: PydanticObjectId) -> DataFrameMetadata:
        dataframe_meta = await DataFrameMetadata.get(dataframe_id)
        if not dataframe_meta:
            raise DataFrameNotFoundError(dataframe_id)
        await dataframe_meta.delete()
        return dataframe_meta


class DataFrameFileCRUD(FileCRUD):
    def __init__(self, user_id):
        self.user_id = user_id

    def _get_csv_path(self, file_id: PydanticObjectId):
        user_path = Path(ROOT_DIR) / str(self.user_id) / "dataframes"
        user_path.mkdir(parents=True, exist_ok=True)
        return user_path / f"{file_id}.csv"

    def upload_csv(self, file_id: PydanticObjectId,
                   file: tempfile.SpooledTemporaryFile) -> FileResponse:
        csv_path = self._get_csv_path(file_id)
        self._upload(csv_path, file)

    def download_csv(self, file_id: PydanticObjectId, filename: str
                     ) -> FileResponse:
        csv_path = self._get_csv_path(file_id)
        if not filename.endswith('.csv'):
            filename += '.csv'
        file_response = self._download(path=csv_path, filename=filename)
        file_response.media_type = "text/csv"
        return file_response

    def read_csv(self, file_id: PydanticObjectId) -> pd.DataFrame:
        csv_path = self._get_csv_path(file_id)
        try:
            data = pd.read_csv(csv_path)
        except FileNotFoundError:
            raise ObjectFileNotFoundError(file_id)
        return data

    def save_csv(self, file_id: PydanticObjectId, data: pd.DataFrame):
        csv_path = self._get_csv_path(file_id)
        data.to_csv(csv_path, index=False)

    def delete_csv(self, file_id: PydanticObjectId):
        csv_path = self._get_csv_path(file_id)
        self._delete(csv_path)

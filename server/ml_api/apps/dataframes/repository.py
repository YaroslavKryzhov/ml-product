from typing import List
from uuid import UUID
from typing import Dict

import pandas as pd
from fastapi.responses import FileResponse
from fastapi import HTTPException, status
from beanie import PydanticObjectId

from ml_api.common.file_manager.base import FileCRUD
from ml_api.apps.dataframes.models import DataFrameMetadata


class DataFrameInfoCRUD:
    def __init__(self, user_id: PydanticObjectId):
        self.user_id = user_id

    async def get(self, dataframe_id: PydanticObjectId) -> DataFrameMetadata:
        dataframe_meta = await DataFrameMetadata.get(dataframe_id)
        if dataframe_meta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dataframe with id {dataframe_id} not found."
            )
        return dataframe_meta

    async def get_all(self) -> List[DataFrameMetadata]:
        dataframe_metas = await DataFrameMetadata.find(DataFrameMetadata.user_id == self.user_id).to_list()
        return dataframe_metas

    async def create(self, filename: str) -> DataFrameMetadata:
        new_obj = DataFrameMetadata(filename=filename, user_id=self.user_id)
        await new_obj.insert()
        return new_obj

    async def update(self, dataframe_id: PydanticObjectId, query: Dict) -> DataFrameMetadata:
        dataframe_meta = await DataFrameMetadata.get(dataframe_id)
        if not dataframe_meta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dataframe with id {dataframe_id} not found."
            )
        return await dataframe_meta.update(query)

    async def delete(self, dataframe_id: PydanticObjectId):
        dataframe_meta = await DataFrameMetadata.get(dataframe_id)
        if not dataframe_meta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dataframe with id {dataframe_id} not found."
            )
        await dataframe_meta.delete()


class DataFrameFileCRUD(FileCRUD):

    def read_csv(self, file_id: PydanticObjectId) -> pd.DataFrame:
        csv_path = self._get_path(file_id)
        try:
            data = pd.read_csv(csv_path)
        except FileNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Dataframe with id {file_id} not found."
            )
        return data

    def download_csv(self, file_id: PydanticObjectId, filename: str) -> FileResponse:
        file_response = self.download(file_id=file_id, filename=filename)
        file_response.media_type = "text/csv"
        return file_response

    def save_csv(self, file_id: PydanticObjectId, data: pd.DataFrame):
        data.to_csv(self._get_path(file_id), index=False)

from typing import List
from beanie import PydanticObjectId

from fastapi.responses import FileResponse
import pandas as pd

from ml_api.apps.dataframes.repository import DataFrameInfoCRUD, DataFrameFileCRUD
from ml_api.apps.dataframes.models import DataFrameMetadata, ColumnTypes


class DataframeFileManagerService:
    """
    Работает с файлами ОС и отвечает за синхронизацию файловой системы с данными в MongoDB
    при добавлении/удалении файлов. Также отвечает за доступ к файлам.
    """
    def __init__(self, user_id):
        self._user_id = user_id
        self.info_repository = DataFrameInfoCRUD(self._user_id)
        self.file_repository = DataFrameFileCRUD(self._user_id)

    # 1: FILE MANAGEMENT OPERATIONS -------------------------------------------
    async def upload_file(self, file, filename: str) -> DataFrameMetadata:
        dataframe_meta = await self.info_repository.create(filename)
        self.file_repository.upload(file_id=dataframe_meta.id, file=file)
        return dataframe_meta

    async def create_file(self, df: pd.DataFrame, filename: str,
                          parent_id: PydanticObjectId = None
                          ) -> DataFrameMetadata:
        dataframe_meta = await self.info_repository.create(filename, parent_id)
        self.file_repository.save_csv(dataframe_meta.id, df)
        return dataframe_meta

    async def download_file(self, dataframe_id: PydanticObjectId
                            ) -> FileResponse:
        dataframe_meta = await self.info_repository.get(dataframe_id)
        response = self.file_repository.download_csv(
            file_id=dataframe_id, filename=dataframe_meta.filename)
        return response

    async def delete_file(self, dataframe_id: PydanticObjectId
                          ) -> DataFrameMetadata:
        dataframe_meta = await self.info_repository.delete(dataframe_id)
        self.file_repository.delete(dataframe_id)
        return dataframe_meta

    async def read_df_from_file(self, dataframe_id: PydanticObjectId
                                ) -> pd.DataFrame:
        return self.file_repository.read_csv(dataframe_id)

    async def write_df_to_file(self, dataframe_id: PydanticObjectId,
                               df: pd.DataFrame) -> None:
        self.file_repository.save_csv(dataframe_id, df)

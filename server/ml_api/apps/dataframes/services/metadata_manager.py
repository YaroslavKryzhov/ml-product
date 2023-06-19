from uuid import UUID
from datetime import datetime

from fastapi import HTTPException, status
import pandas as pd

import ml_api.apps.dataframes.schemas as schemas
from ml_api.apps.dataframes.repository import DataFrameInfoCRUD
import ml_api.apps.dataframes.utils as utils

from ml_api.apps.dataframes.services.file_manager import DataframeFileManagerService


class DataframeMetadataManagerService:
    def __init__(self, db, user_id):
        self._db = db
        self._user_id = user_id
        self.info_repository = DataFrameInfoCRUD(self._db, self._user_id)
        self.file_service = DataframeFileManagerService(self._db,
                                                        self._user_id)

    # 3: SET OPERATIONS -------------------------------------------------------

        # # TODO: связность кода + некрасивая строка = нужен рефакторинг
        # DataframeMetadataManagerService(self._db, self._user_id)._define_start_column_types(dataframe_meta.id)

    def _define_start_column_types(self, dataframe_id: UUID) -> schemas.ColumnTypes:
        df = self.file_service.read_file_to_df(dataframe_id)
        column_types = utils._define_column_types(df)
        self.set_column_types(dataframe_id, column_types)

    def get_dataframe_column_types(self,
                                    dataframe_id: UUID) -> schemas.ColumnTypes:
        return self.info_repository.get(
            dataframe_id).column_types

    def set_column_types(self, dataframe_id: UUID,
                         column_types: schemas.ColumnTypes):
        query = {
            'column_types': column_types,
            'updated_at': str(datetime.now())
        }
        self.info_repository.update(dataframe_id, query)

    def set_target_column(self, dataframe_id: UUID, target_column: str):
        column_types = self.get_dataframe_column_types(dataframe_id)
        if (target_column in column_types.numeric or
                target_column in column_types.categorical):
            column_types.target = target_column
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Column {target_column} not found in df.columns"
            )
        self.set_column_types(dataframe_id, column_types)

    def change_column_type_to_categorical(self, dataframe_id: UUID,
                                          column_name: str):
        column_types = self.get_dataframe_column_types(dataframe_id)
        try:
            column_types.numeric.remove(column_name)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Column {column_name} not found in numeric columns."
            )
        column_types.categorical.append(column_name)
        self.set_column_types(dataframe_id, column_types)

    def change_column_type_to_numeric(self, dataframe_id: UUID,
                                      column_name: str):
        df = self.file_service.read_file_to_df(dataframe_id)
        column_types = self.get_dataframe_column_types(dataframe_id)
        try:
            column_types.categorical.remove(column_name)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Column {column_name} not found in categorical columns."
            )
        column_types.numeric.append(column_name)

        try:
            df[column_name] = pd.to_numeric(df[column_name])
            self.file_service.save_df_to_file(dataframe_id, df)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Column {column_name} can't be parsed like numeric."
            )
        self.set_column_types(dataframe_id, column_types)
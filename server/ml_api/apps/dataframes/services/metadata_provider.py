from uuid import UUID
from typing import List

from fastapi import HTTPException, status
import pandas as pd

import ml_api.apps.dataframes.schemas as schemas
from ml_api.apps.dataframes.repository import DataFrameInfoCRUD
import ml_api.apps.dataframes.utils as utils

from ml_api.apps.dataframes.services.file_manager import DataframeFileManagerService


class DataframeMetadataProviderService:
    def __init__(self, db, user_id):
        self._db = db
        self._user_id = user_id
        self.info_repository = DataFrameInfoCRUD(self._db, self._user_id)
        self.file_service = DataframeFileManagerService(self._db, self._user_id)

    # 2: GET OPERATIONS -------------------------------------------------------
    def get_dataframe_info(self, dataframe_id: UUID) -> schemas.DataFrameInfo:
        return self.info_repository.get(dataframe_id)

    def get_dataframe_column_types(self,
                                    dataframe_id: UUID) -> schemas.ColumnTypes:
        return self.info_repository.get(
            dataframe_id).column_types

    def get_all_dataframes_info(self) -> List[schemas.DataFrameInfo]:
        return self.info_repository.get_all()

    def get_dataframe_statistic_description(
            self, filename: str
    ) -> schemas.DataFrameDescription:
        df = self.file_service.read_file_to_df(filename)
        return utils._get_dataframe_statistic_description_data(df)

    def get_dataframe_with_pagination(
            self, dataframe_id: UUID, page: int = 1, rows_on_page: int = 50
    ) -> schemas.ReadDataFrameResponse:
        df = self.file_service.read_file_to_df(dataframe_id)
        length = len(df)
        pages_count = (length - 1) // rows_on_page + 1
        start_index = (page - 1) * rows_on_page
        stop_index = page * rows_on_page
        if stop_index < length:
            return {
                'total': pages_count,
                'records': df.iloc[start_index:stop_index]
                .fillna("")
                .to_dict('list'),
            }
        elif start_index < length:
            return {
                'total': pages_count,
                'records': df.iloc[start_index:]
                .fillna("")
                .to_dict('list'),
            }
        else:
            return {
                'total': pages_count,
                'records': pd.DataFrame().fillna("").to_dict('list'),
            }

    def get_dataframe_columns(self, dataframe_id: UUID) -> List[str]:
        return self.file_service.read_file_to_df(dataframe_id).columns.to_list()

    def get_dataframe_column_statistics(
            self, dataframe_id: UUID, bins: int = 10
    ) -> List[schemas.ColumnDescription]:
        result = []
        df = self.file_service.read_file_to_df(dataframe_id)
        column_types = self.get_dataframe_column_types(dataframe_id)
        for column_name in column_types.numeric:
            result.append(utils._get_column_histogram_data(
                df=df, column_name=column_name, bins=bins))
        for column_name in column_types.categorical:
            result.append(utils._get_column_value_counts_data
                          (df=df, column_name=column_name))
        return result

    def get_feature_target_df(self, dataframe_id: UUID):
        df = self.file_service.read_file_to_df(dataframe_id)
        feature_columns, target_column = self.get_feature_target_column_names(
            dataframe_id=dataframe_id)
        if target_column is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Dataframe with id {dataframe_id} has no target column"
            )
        features = df.drop(target_column, axis=1)
        target = df[target_column]
        if features.columns.tolist().sort() != feature_columns.sort():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Feature columns in dataframe info with id "
                       f"{dataframe_id} not equal to real in Dataframe"
            )
        return features, target

    def get_feature_df(self, dataframe_id: UUID):
        df = self.file_service.read_file_to_df(dataframe_id)
        feature_columns, target_column = self.get_feature_target_column_names(
            dataframe_id=dataframe_id)

        if df.columns.tolist().sort() != feature_columns.sort():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Feature columns in dataframe info with id "
                       f"{dataframe_id} not equal to real in Dataframe"
            )
        return df

    def get_feature_target_column_names(self, dataframe_id: UUID
                                        ) -> (List, str):
        column_types = self.get_dataframe_column_types(dataframe_id)
        target_column = column_types.target

        feature_columns = column_types.categorical + column_types.numeric
        # TODO: think about categorical (catboost only, i think)
        if target_column is not None:
            try:
                feature_columns.remove(target_column)
            except Exception as e: # TODO: костыль для закрытия бага
                print(e)
        return feature_columns, target_column

from beanie import PydanticObjectId
from fastapi import HTTPException, status
import pandas as pd

from ml_api.apps.dataframes.services.file_manager import DataframeFileManagerService
from ml_api.apps.dataframes.services.metadata_manager import DataframeMetadataManagerService
from ml_api.apps.dataframes.models import ColumnTypes, DataFrameMetadata
from ml_api.apps.dataframes import utils


class DataframeManagerService:
    """
    Работает с pd.Dataframe и отвечает за обработку и изменение данных внутри pandas-датафреймов.
    """
    def __init__(self, user_id):
        self._user_id = user_id
        self.metadata_service = DataframeMetadataManagerService(self._user_id)
        self.file_service = DataframeFileManagerService(self._user_id)

    # 2: GET OPERATIONS -------------------------------------------------------
    async def add_dataframe(self, file, filename: str) -> DataFrameMetadata:
        dataframe_meta = await self.file_service.upload_file(file, filename)
        dataframe_meta_updated = await self._define_and_set_initial_column_types(dataframe_meta.id)
        return dataframe_meta_updated

    async def _define_and_set_initial_column_types(self, dataframe_id: PydanticObjectId) -> ColumnTypes:
        df = await self.file_service.read_df_from_file(dataframe_id)
        column_types = utils._define_column_types(df)
        return await self.metadata_service.set_column_types(dataframe_id, column_types)

    async def change_column_type_to_categorical(self, dataframe_id: PydanticObjectId,
                                          column_name: str):
        column_types = await self.metadata_service.get_dataframe_column_types(
            dataframe_id)
        df = await self.file_service.read_df_from_file(dataframe_id)
        try:
            column_types.numeric.remove(column_name)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Column {column_name} not found in numeric columns."
            )
        column_types.categorical.append(column_name)

        try:
            df[column_name] = df[column_name].astype(str)
            if df[column_name].value_counts().shape[0] > 1000:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Column {column_name} can't be parsed like categorical.(Has too much values: >1000)"
                )
            await self.file_service.write_df_to_file(dataframe_id, df)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Column {column_name} can't be parsed like categorical."
            )
        return await self.metadata_service.set_column_types(dataframe_id, column_types)

    async def change_column_type_to_numeric(self, dataframe_id: PydanticObjectId,
                                      column_name: str):
        column_types = await self.metadata_service.get_dataframe_column_types(
            dataframe_id)
        df = await self.file_service.read_df_from_file(dataframe_id)
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
            await self.file_service.write_df_to_file(dataframe_id, df)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Column {column_name} can't be parsed like numeric."
            )
        return await self.metadata_service.set_column_types(dataframe_id, column_types)

    async def get_feature_df(self, dataframe_id: PydanticObjectId):
        # Todo: Странная логика обработки target
        feature_columns, target_column = await self.metadata_service.get_feature_target_column_names(
            dataframe_id=dataframe_id)
        df = await self.file_service.read_df_from_file(dataframe_id)

        if df.columns.tolist().sort() != feature_columns.sort():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Feature columns in dataframe info with id "
                       f"{dataframe_id} not equal to real in Dataframe"
            )
        return df

    async def get_feature_target_df(self, dataframe_id: PydanticObjectId):
        feature_columns, target_column = await self.metadata_service.get_feature_target_column_names(
            dataframe_id=dataframe_id)
        df = await self.file_service.read_df_from_file(dataframe_id)

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

from typing import List, Union, Any

from fastapi import HTTPException, status
from beanie import PydanticObjectId

from ml_api.apps.dataframes.repository import DataFrameInfoCRUD
from ml_api.apps.dataframes.models import DataFrameMetadata, ColumnTypes, PipelineElement
from ml_api.apps.dataframes import specs


class DataframeMetadataManagerService:
    """
    Работает с данными в MongoDB, обеспечивает доступ и управление метадатой.
    """
    def __init__(self, user_id):
        self._user_id = user_id
        self.info_repository = DataFrameInfoCRUD(self._user_id)

    # 3: SET OPERATIONS -------------------------------------------------------

    async def get_dataframe_meta(self, dataframe_id: PydanticObjectId
                                 ) -> DataFrameMetadata:
        return await self.info_repository.get(dataframe_id)

    async def get_all_dataframes_meta(self) -> List[DataFrameMetadata]:
        return await self.info_repository.get_all()

    async def get_dataframe_column_types(self, dataframe_id: PydanticObjectId) -> ColumnTypes:
        dataframe_meta = await self.get_dataframe_meta(dataframe_id)
        return dataframe_meta.feature_columns_types

    async def get_feature_target_column_names(self, dataframe_id: PydanticObjectId
                                        ) -> (List[str], Union[str, None]):
        dataframe_meta = await self.get_dataframe_meta(dataframe_id)
        column_types = dataframe_meta.feature_columns_types
        target_column = dataframe_meta.target
        feature_columns = column_types.categorical + column_types.numeric
        if target_column:
            feature_columns.remove(target_column)
        return feature_columns, target_column

    async def get_dataframe_pipeline(self, dataframe_id: PydanticObjectId) -> List[PipelineElement]:
        dataframe_meta = await self.get_dataframe_meta(dataframe_id)
        return dataframe_meta.pipeline

    async def set_filename(self, dataframe_id: PydanticObjectId, new_filename: str) -> DataFrameMetadata:
        query = {"$set": {DataFrameMetadata.filename: new_filename}}
        return await self.info_repository.update(dataframe_id, query)

    async def set_column_types(self, dataframe_id: PydanticObjectId, column_types: ColumnTypes):
        query = {"$set": {'feature_columns_types': column_types}}
        return await self.info_repository.update(dataframe_id, query)

    async def set_pipeline(self, dataframe_id: PydanticObjectId, pipeline: List[PipelineElement]):
        query = {"$set": {'pipeline': pipeline}}
        return await self.info_repository.update(dataframe_id, query)

    async def add_method_to_pipeline(self, dataframe_id: PydanticObjectId,
                         function_name: specs.AvailableFunctions, params: Any = None):
        pipeline = await self.get_dataframe_pipeline(dataframe_id)
        pipeline.append(PipelineElement(function_name=function_name, params=params))
        return await self.set_pipeline(dataframe_id, pipeline)

    async def set_target_feature(self, dataframe_id: PydanticObjectId, target_feature: str):
        column_types = await self.get_dataframe_column_types(dataframe_id)
        if (target_feature in column_types.numeric or
                target_feature in column_types.categorical):
            query = {"$set": {'target_feature': target_feature}}
            return await self.info_repository.update(dataframe_id, query)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Column {target_feature} not found in df.columns"
            )

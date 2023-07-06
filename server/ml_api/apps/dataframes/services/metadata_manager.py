from typing import List, Optional

from beanie import PydanticObjectId

from ml_api.apps.dataframes.repository import DataFrameInfoCRUD
from ml_api.apps.dataframes.models import DataFrameMetadata, ColumnTypes, ApplyMethodParams
from ml_api.apps.dataframes.errors import ColumnNotFoundMetadataError


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

    async def get_column_types(self, dataframe_id: PydanticObjectId
                               ) -> ColumnTypes:
        dataframe_meta = await self.get_dataframe_meta(dataframe_id)
        return dataframe_meta.feature_columns_types

    async def get_filename(self, dataframe_id: PydanticObjectId
                           ) -> ColumnTypes:
        dataframe_meta = await self.get_dataframe_meta(dataframe_id)
        return dataframe_meta.filename

    async def get_parent_id(self, dataframe_id: PydanticObjectId
                            ) -> Optional[PydanticObjectId]:
        dataframe_meta = await self.get_dataframe_meta(dataframe_id)
        return dataframe_meta.parent_id

    async def get_pipeline(self, dataframe_id: PydanticObjectId
                           ) -> List[ApplyMethodParams]:
        dataframe_meta = await self.get_dataframe_meta(dataframe_id)
        return dataframe_meta.pipeline

    async def set_filename(self, dataframe_id: PydanticObjectId,
                           new_filename: str) -> DataFrameMetadata:
        query = {"$set": {DataFrameMetadata.filename: new_filename}}
        return await self.info_repository.update(dataframe_id, query)

    async def set_column_types(self, dataframe_id: PydanticObjectId,
                               column_types: ColumnTypes) -> DataFrameMetadata:
        query = {"$set": {'feature_columns_types': column_types}}
        return await self.info_repository.update(dataframe_id, query)

    async def set_pipeline(self, dataframe_id: PydanticObjectId,
            pipeline: List[ApplyMethodParams]) -> DataFrameMetadata:
        query = {"$set": {'pipeline': pipeline}}
        return await self.info_repository.update(dataframe_id, query)

    async def set_target_feature(self, dataframe_id: PydanticObjectId,
                                 target_feature: str) -> DataFrameMetadata:
        column_types = await self.get_column_types(dataframe_id)
        if not (target_feature in column_types.numeric or
                target_feature in column_types.categorical):
            raise ColumnNotFoundMetadataError(target_feature)
        query = {"$set": {'target_feature': target_feature}}
        return await self.info_repository.update(dataframe_id, query)

    async def unset_target_feature(self, dataframe_id: PydanticObjectId
                                   ) -> DataFrameMetadata:
        query = {"$set": {'target_feature': None}}
        return await self.info_repository.update(dataframe_id, query)

    async def set_parent_id(self, dataframe_id,
                            new_parent_id: Optional[PydanticObjectId]
                            ) -> DataFrameMetadata:
        query = {"$set": {'parent_id': new_parent_id}}
        return await self.info_repository.update(dataframe_id, query)

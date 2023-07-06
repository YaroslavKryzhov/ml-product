from typing import List, Dict

from beanie import PydanticObjectId

from ml_api.apps.dataframes import schemas
import ml_api.apps.dataframes.utils as utils

from ml_api.apps.dataframes.services.file_manager import DataframeFileManagerService
from ml_api.apps.dataframes.services.metadata_manager import DataframeMetadataManagerService


class DataframeStatisticsProviderService:
    """
    Отвечает за предоставление клиенту данных, необходимых для отображения
    датафрейма (страница Датафрейма на фронтенд-клиенте).
    """
    def __init__(self, user_id):
        self._user_id = user_id
        self.metadata_service = DataframeMetadataManagerService(self._user_id)
        self.file_service = DataframeFileManagerService(self._user_id)

    async def get_dataframe_with_pagination(self,
                                            dataframe_id: PydanticObjectId,
                                            page: int = 1,
                                            rows_on_page: int = 50
                                            ) -> schemas.ReadDataFrameResponse:
        await self.metadata_service.get_dataframe_meta(dataframe_id)
        df = await self.file_service.read_df_from_file(dataframe_id)
        return utils._get_dataframe_with_pagination(df, page, rows_on_page)

    async def get_dataframe_column_statistics(self,
                                              dataframe_id: PydanticObjectId,
                                              bins: int = 10
                                              ) -> List[schemas.ColumnDescription]:
        result = []
        dataframe_meta = await self.metadata_service.get_dataframe_meta(dataframe_id)
        df = await self.file_service.read_df_from_file(dataframe_id)
        column_types = dataframe_meta.feature_columns_types
        for column_name in column_types.numeric:
            result.append(utils._get_numeric_column_statistics(
                df=df, column_name=column_name, bins=bins))
        for column_name in column_types.categorical:
            result.append(utils._get_categorical_column_statistics
                          (df=df, column_name=column_name))
        return result

    async def get_correlation_matrix(self, dataframe_id: PydanticObjectId
                                     ) -> Dict[str, Dict[str, float]]:
        await self.metadata_service.get_dataframe_meta(dataframe_id)
        df = await self.file_service.read_df_from_file(dataframe_id)
        return df.corr().to_dict()

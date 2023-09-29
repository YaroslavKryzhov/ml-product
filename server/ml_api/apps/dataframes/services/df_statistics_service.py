from typing import List, Dict

from beanie import PydanticObjectId

from ml_api.apps.dataframes import schemas
import ml_api.apps.dataframes.utils as utils

from ml_api.apps.dataframes.repositories.repository_manager import DataframeRepositoryManager


class DataframeStatisticsService:
    """
    Отвечает за предоставление клиенту данных, необходимых для отображения
    датафрейма (страница Датафрейма на фронтенд-клиенте).
    """
    def __init__(self, user_id):
        self._user_id = user_id
        self.repository = DataframeRepositoryManager(self._user_id)

    async def get_dataframe_with_pagination(self,
                                            dataframe_id: PydanticObjectId,
                                            page: int = 1,
                                            rows_on_page: int = 50
                                            ) -> schemas.ReadDataFrameResponse:
        df = await self.repository.read_pandas_dataframe(dataframe_id)
        return utils._get_dataframe_with_pagination(df, page, rows_on_page)

    async def get_dataframe_column_statistics(self,
                                              dataframe_id: PydanticObjectId,
                                              bins: int = 10
                                              ) -> List[schemas.ColumnDescription]:
        result = []
        df = await self.repository.read_pandas_dataframe(dataframe_id)
        column_types = await self.repository.get_feature_column_types(dataframe_id)
        for column_name in column_types.numeric:
            result.append(utils._get_numeric_column_statistics(
                df=df, column_name=column_name, bins=bins))
        for column_name in column_types.categorical:
            result.append(utils._get_categorical_column_statistics
                          (df=df, column_name=column_name))
        return result

    async def get_correlation_matrix(self, dataframe_id: PydanticObjectId
                                     ) -> Dict[str, Dict[str, float]]:
        df = await self.repository.read_pandas_dataframe(dataframe_id)
        return df.corr().to_dict()

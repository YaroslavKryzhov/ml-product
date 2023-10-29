from typing import List, Optional, Dict

from beanie import PydanticObjectId
import pandas as pd

from ml_api.apps.dataframes.repositories.repository_manager import \
    DataframeRepositoryManager
from ml_api.apps.dataframes.model import DataFrameMetadata
from ml_api.apps.dataframes import utils, schemas, errors
from ml_api.apps.ml_models.facade import ModelServiceFacade


class DataframeService:
    """
    Работает с pd.Dataframe и отвечает за обработку и изменение данных внутри pandas-датафреймов.
    """

    def __init__(self, user_id):
        self._user_id = user_id
        self.repository = DataframeRepositoryManager(self._user_id)
        self.models_service = ModelServiceFacade(self._user_id)

    async def _define_initial_column_types(self, dataframe_id: PydanticObjectId
                                           ) -> schemas.ColumnTypes:
        df = await self.repository.read_pandas_dataframe(dataframe_id)
        df, column_types = utils.convert_dtypes(df)
        self._check_columns_consistency(
            df, column_types.numeric + column_types.categorical)
        await self.repository.save_pandas_dataframe(dataframe_id, df)
        return await self.repository.set_feature_column_types(
            dataframe_id, column_types)

    def _check_columns_consistency(self, df: pd.DataFrame, columns_list: List):
        # Проверка на то, что DataFrame содержит ожидаемые столбцы
        df_columns_list = df.columns.tolist()
        if sorted(df_columns_list) != sorted(columns_list):
            raise errors.ColumnsNotEqualCriticalError(df_columns_list,
                                                      columns_list)

    # 1: CREATE OPERATIONS ----------------------------------------------------
    async def upload_new_dataframe(self, file,
                                   filename: str) -> DataFrameMetadata:
        dataframe_meta = await self.repository.upload_dataframe(file, filename)
        return await self._define_initial_column_types(dataframe_meta.id)

    async def save_transformed_dataframe(
            self,
            changed_df_meta: DataFrameMetadata,
            new_df: pd.DataFrame, method_name: str = 'modified'
    ) -> DataFrameMetadata:
        changed_df_meta.parent_id = changed_df_meta.id
        changed_df_meta.filename = f"{changed_df_meta.filename}_{method_name}"
        while True:
            try:
                meta_created = await self.repository.save_as_new_dataframe(
                    new_df, changed_df_meta)
                return meta_created
            except errors.FilenameExistsUserError:
                changed_df_meta.filename = f"{changed_df_meta.filename}_{utils.get_random_number()}"

    # 2: GET OPERATIONS -------------------------------------------------------
    async def download_dataframe(self, dataframe_id):
        return await self.repository.download_dataframe(dataframe_id)

    async def get_dataframe_meta(self, dataframe_id) -> DataFrameMetadata:
        return await self.repository.get_dataframe_meta(dataframe_id)

    async def get_active_dataframes_meta(self) -> List[DataFrameMetadata]:
        return await self.repository.get_active_dataframes_meta()

    async def get_feature_column_types(self, dataframe_id):
        return await self.repository.get_feature_column_types(dataframe_id)

    async def get_dataframe_with_pagination(self, dataframe_id: PydanticObjectId,
             page: int = 1, rows_on_page: int = 50) -> schemas.ReadDataFrameResponse:
        df = await self.repository.read_pandas_dataframe(dataframe_id)
        return utils._get_dataframe_with_pagination(df, page, rows_on_page)

    async def get_dataframe_column_statistics(self, dataframe_id: PydanticObjectId,
            bins: int = 10) -> List[schemas.ColumnDescription]:
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

    async def get_feature_target_column_names(self,
                                              dataframe_id: PydanticObjectId) -> (
    List[str], Optional[str]):
        """Returns list of feature columns and target column name.
        If target column is not set, returns None instead of target column name.
        If feature columns contain categorical column, raises ColumnNotNumericError."""
        dataframe_meta = await self.repository.get_dataframe_meta(dataframe_id)
        column_types = dataframe_meta.feature_columns_types
        target_column = dataframe_meta.target_feature
        if target_column is not None:
            # если целевой признак задан, убираем его из ColumnTypes
            if target_column in column_types.numeric:
                column_types.numeric.remove(target_column)
            elif target_column in column_types.categorical:
                column_types.categorical.remove(target_column)
            else:
                # если его нет в ColumnTypes - поднимаем 500-ую
                raise errors.UnknownTargetCriticalError(dataframe_id)
        if len(column_types.categorical) > 0:
            # если среди столбцов остались категориальные
            # (после удаления таргета) - поднимаем 500-ую
            raise errors.CategoricalColumnFoundCriticalError(dataframe_id,
                column_types.categorical)
        if len(column_types.categorical) == 0 and len(column_types.numeric) == 0:
            raise errors.ColumnTypesNotDefinedCriticalError(dataframe_id)
        return column_types.numeric, target_column

    async def get_feature_target_df_supervised(self,
                                               dataframe_id: PydanticObjectId) -> (
    pd.DataFrame, pd.Series):
        features, target = await self.get_feature_target_df(dataframe_id)
        if target is None:
            raise errors.TargetNotFoundSupervisedLearningError(dataframe_id)
        return features, target

    async def get_feature_target_df(self, dataframe_id: PydanticObjectId
                                    ) -> (pd.DataFrame, Optional[pd.Series]):
        feature_columns, target_column = await self.get_feature_target_column_names(
            dataframe_id=dataframe_id)
        df = await self.repository.read_pandas_dataframe(dataframe_id)
        if target_column is not None:
            # если есть таргет - возвращаем его отдельно
            df_columns_list = feature_columns + [target_column]
            self._check_columns_consistency(df, df_columns_list)
            features = df[feature_columns]
            target = df[target_column]
            return features, target
        else:
            # если таргета нет - возвращаем вместо него None
            self._check_columns_consistency(df, feature_columns)
            return df, None

    # 3: UPDATE OPERATIONS ----------------------------------------------------
    async def set_filename(self, dataframe_id, new_filename):
        return await self.repository.set_filename(dataframe_id, new_filename)

    async def set_target_feature(self, dataframe_id: PydanticObjectId,
                                 target_feature: str) -> DataFrameMetadata:
        column_types = await self.repository.get_feature_column_types(
            dataframe_id)
        if not (target_feature in column_types.numeric or
                target_feature in column_types.categorical):
            raise errors.SetTargetNotFoundInMetadataError(
                dataframe_id, target_feature)
        return await self.repository.set_target_feature(dataframe_id,
                                                        target_feature)

    async def unset_target_feature(self, dataframe_id: PydanticObjectId
                                   ) -> DataFrameMetadata:
        target_feature = self.repository.get_target_feature(dataframe_id)
        if target_feature is None:
            raise errors.UnsetTargetFeatureError(dataframe_id)
        return await self.repository.set_target_feature(dataframe_id, None)

    async def move_dataframe_to_root(self, dataframe_id: PydanticObjectId
                                     ) -> DataFrameMetadata:
        dataframe_meta = await self.repository.get_dataframe_meta(dataframe_id)
        if dataframe_meta.is_prediction:
            raise errors.DataFrameIsPredictionError(dataframe_id)
        if dataframe_meta.parent_id is None:
            raise errors.DataFrameAlreadyRootError(dataframe_id)
        dataframe_meta = await self.repository.set_parent_id(dataframe_id,
                                                             None)
        return dataframe_meta

    async def move_prediction_to_active(
            self, model_id: PydanticObjectId, dataframe_id: PydanticObjectId
    ) -> DataFrameMetadata:
        dataframe_meta = await self.repository.get_dataframe_meta(dataframe_id)
        if not dataframe_meta.is_prediction:
            raise errors.DataFrameIsNotPredictionError(dataframe_id)
        await self.models_service.remove_from_model_predictions(
            model_id, dataframe_id)
        dataframe_meta = await self.repository.set_is_prediction(
            dataframe_id, False)
        return await self._define_initial_column_types(dataframe_meta.id)

    # 4: DELETE OPERATIONS ----------------------------------------------------
    async def delete_dataframe(self, dataframe_id: PydanticObjectId
                               ) -> DataFrameMetadata:
        dataframe_meta = await self.repository.get_dataframe_meta(dataframe_id)
        if dataframe_meta.is_prediction:
            raise errors.DataFrameIsPredictionError(dataframe_id)
        child_dataframes = await self.repository.get_dataframe_metas_by_parent_id(
            dataframe_id)
        for child_dataframe in child_dataframes:
            await self.delete_dataframe(child_dataframe.id)
        await self.models_service.delete_models_by_dataframe(dataframe_id)
        dataframe_meta = await self.repository.delete_dataframe(dataframe_id)
        return dataframe_meta

    async def delete_prediction(self, model_id: PydanticObjectId,
                                prediction_id: PydanticObjectId
                                ) -> DataFrameMetadata:
        dataframe_meta = await self.repository.get_dataframe_meta(prediction_id)
        if not dataframe_meta.is_prediction:
            raise errors.DataFrameIsNotPredictionError(prediction_id)
        await self.models_service.remove_from_model_predictions(
            model_id, prediction_id)
        dataframe_meta = await self.repository.delete_dataframe(prediction_id)
        return dataframe_meta

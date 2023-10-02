from typing import List, Optional

from beanie import PydanticObjectId
import pandas as pd

from ml_api.apps.dataframes.repositories.repository_manager import \
    DataframeRepositoryManager
from ml_api.apps.dataframes.models import DataFrameMetadata
from ml_api.apps.dataframes import utils, specs, schemas, errors


class DataframeService:
    """
    Работает с pd.Dataframe и отвечает за обработку и изменение данных внутри pandas-датафреймов.
    """

    def __init__(self, user_id):
        self._user_id = user_id
        self.repository = DataframeRepositoryManager(self._user_id)

    async def upload_new_dataframe(self, file,
                                   filename: str) -> DataFrameMetadata:
        dataframe_meta = await self.repository.upload_dataframe(file, filename)
        return await self._define_initial_column_types(dataframe_meta.id)

    async def _define_initial_column_types(self, dataframe_id: PydanticObjectId
                                           ) -> schemas.ColumnTypes:
        df = await self.repository.read_pandas_dataframe(dataframe_id)
        df, column_types = utils.convert_dtypes(df)
        self._check_columns_consistency(
            df, column_types.numeric + column_types.categorical)
        await self.repository.save_pandas_dataframe(dataframe_id, df)
        return await self.repository.set_feature_column_types(
            dataframe_id, column_types)

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
                raise errors.TargetNotFoundCriticalError(dataframe_id)
        if len(column_types.categorical) > 0:
            # если среди столбцов остались категориальные
            # (после удаления таргета) - поднимаем 500-ую
            raise errors.CategoricalColumnFoundCriticalError(
                column_types.categorical)
        if len(column_types.categorical) == 0 and len(column_types.numeric) == 0:
            raise errors.ColumnTypesNotDefined(dataframe_id)
        return column_types.numeric, target_column

    async def get_feature_target_df_supervised(self,
                                               dataframe_id: PydanticObjectId) -> (
    pd.DataFrame, pd.Series):
        features, target = await self.get_feature_target_df(dataframe_id)
        if target is None:
            raise errors.TargetNotFoundError(dataframe_id)
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

    def _check_columns_consistency(self, df: pd.DataFrame, columns_list: List):
        # Проверка на то, что DataFrame содержит ожидаемые столбцы
        df_columns_list = df.columns.tolist()
        if sorted(df_columns_list) != sorted(columns_list):
            raise errors.ColumnsNotEqualCriticalError(df_columns_list,
                                                      columns_list)

    async def convert_column_to_new_type(
            self, dataframe_id: PydanticObjectId,
            column_name: str, new_type: specs.ColumnType
    ) -> DataFrameMetadata:
        column_types = await self.repository.get_feature_column_types(dataframe_id)
        column_types = self._change_column_type(column_types, column_name, new_type)

        df = await self.repository.read_pandas_dataframe(dataframe_id)
        self._check_columns_consistency(df,
                            column_types.numeric + column_types.categorical)
        converted_column = self._convert_column_to_new_type(df[column_name],
                                                            new_type)
        df[column_name] = converted_column
        await self.repository.save_pandas_dataframe(dataframe_id, df)
        return await self.repository.set_feature_column_types(dataframe_id,
                                                              column_types)

    def _convert_column_to_new_type(self, column: pd.Series,
                                    new_type: specs.ColumnType) -> pd.Series:
        try:
            if new_type == specs.ColumnType.CATEGORICAL:
                converted_column = utils._convert_column_to_categorical(column)
                if converted_column.nunique() > 1000:
                    raise errors.ColumnCantBeParsedError(column.name,
                                                         "categorical",
                                                         "too many unique values")
            else:  # new_type == specs.ColumnType.NUMERIC
                converted_column = utils._convert_column_to_numeric(
                    column)
        except ValueError:
            raise errors.ColumnCantBeParsedError(column.name, new_type.value,
                                                 "invalid values")
        return converted_column.convert_dtypes()

    def _change_column_type(self, column_types: schemas.ColumnTypes,
            column_name: str, new_type: specs.ColumnType) -> schemas.ColumnTypes:
        # Определяем список исходного типа и типа, на который нужно изменить
        source_list, target_list = (
            (column_types.categorical, column_types.numeric)
            if new_type == specs.ColumnType.NUMERIC
            else (column_types.numeric, column_types.categorical)
        )
        # Пытаемся переместить column_name из source_list в target_list
        try:
            source_list.remove(column_name)
            target_list.append(column_name)
        except ValueError:
            raise errors.ColumnNotFoundMetadataError(column_name,
                 'categorical' if new_type == specs.ColumnType.NUMERIC else 'numeric')
        return column_types

    async def set_target_feature(self, dataframe_id: PydanticObjectId,
                                 target_feature: str) -> DataFrameMetadata:
        column_types = await self.repository.get_feature_column_types(
            dataframe_id)
        if not (target_feature in column_types.numeric or
                target_feature in column_types.categorical):
            raise errors.ColumnNotFoundMetadataError(target_feature)
        return await self.repository.set_target_feature(dataframe_id,
                                                        target_feature)

    async def unset_target_feature(self, dataframe_id: PydanticObjectId
                                   ) -> DataFrameMetadata:
        target_feature = self.repository.get_target_feature(dataframe_id)
        if target_feature is None:
            raise errors.TargetNotFoundError(dataframe_id)
        return await self.repository.set_target_feature(dataframe_id, None)

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

    async def save_predictions_dataframe(self,
                                         df_filename: str,
                                         pred_df: pd.DataFrame,
                                         ) -> DataFrameMetadata:
        while True:
            try:
                meta_created = await self.repository.save_prediction_dataframe(
                    pred_df, df_filename)
                return meta_created
            except errors.FilenameExistsUserError:
                df_filename = f"{df_filename}_{utils.get_random_number()}"

    async def move_prediction_to_active(self, dataframe_id: PydanticObjectId
                                     ) -> DataFrameMetadata:
        dataframe_meta = await self.repository.get_dataframe_meta(dataframe_id)
        if not dataframe_meta.is_prediction:
            raise errors.DataFrameIsNotPredictionError(dataframe_id)
        dataframe_meta = await self.repository.set_is_prediction(
            dataframe_id, False)
        return await self._define_initial_column_types(dataframe_meta.id)

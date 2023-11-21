from typing import List, Optional

import pandas as pd
from beanie import PydanticObjectId

from ml_api.apps.dataframes import specs, schemas, errors
from ml_api.apps.dataframes.model import DataFrameMetadata
from ml_api.apps.dataframes.repositories.repository_manager import \
    DataframeRepositoryManager
from ml_api.apps.dataframes.services.processors.methods_applier import \
    MethodsApplier
from ml_api.apps.dataframes.services.processors.feature_selector import \
    FeatureSelector
from ml_api.apps.dataframes.services.dataframe_service import \
    DataframeService


class DataframeMethodsService:
    """
    Применяет функции к датафрейму и сохраняет результаты в базу.
    """

    def __init__(self, user_id):
        self._user_id = user_id
        self.repository = DataframeRepositoryManager(self._user_id)
        self.dataframe_service = DataframeService(self._user_id)

    def _check_columns_consistency(self, df: pd.DataFrame, columns_list: List):
        # Проверка на то, что DataFrame содержит ожидаемые столбцы
        df_columns_list = df.columns.tolist()
        if sorted(df_columns_list) != sorted(columns_list):
            raise errors.ColumnsNotEqualCriticalError(df_columns_list,
                                                      columns_list)

    async def _get_df_and_meta(self, dataframe_id: PydanticObjectId):
        dataframe_meta = await self.repository.get_dataframe_meta(dataframe_id)
        df = await self.repository.read_pandas_dataframe(dataframe_id)
        columns_list = dataframe_meta.feature_columns_types.numeric + \
            dataframe_meta.feature_columns_types.categorical
        self._check_columns_consistency(df, columns_list)
        return dataframe_meta, df

    async def get_feature_target_column_names(self,
                                              dataframe_id: PydanticObjectId
                                              ) -> (List[str], Optional[str]):
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
                                               dataframe_id: PydanticObjectId
                                               ) -> (pd.DataFrame, pd.Series):
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

    async def process_feature_importances(
            self,
            dataframe_id: PydanticObjectId,
            task_type: specs.FeatureSelectionTaskType,
            feature_selection_params: List[schemas.SelectorMethodParams]
    ) -> schemas.FeatureSelectionSummary:
        await self.dataframe_service._ensure_not_prediction(dataframe_id)
        features, target = await self.get_feature_target_df_supervised(
            dataframe_id)
        selector = FeatureSelector(
            features, target, task_type, feature_selection_params)
        await self.repository.set_feature_importance_report(
            dataframe_id, selector.get_empty_summary())
        try:
            summary = selector.get_summary()
            await self.repository.set_feature_importance_report(
                dataframe_id, summary)
            return summary
        except Exception:
            await self.repository.set_feature_importance_report(
                dataframe_id, None)
            raise

    async def apply_change_columns_type(self, dataframe_id: PydanticObjectId,
                            method_params: List[schemas.ApplyMethodParams]
                            ) -> DataFrameMetadata:
        await self.dataframe_service._ensure_not_prediction(dataframe_id)
        dataframe_meta, df = await self._get_df_and_meta(dataframe_id)

        new_df, new_meta = await self._apply_methods_to_df(
            df, dataframe_meta, method_params)

        await self.repository.save_pandas_dataframe(dataframe_id, new_df)
        await self.repository.set_feature_column_types(
            dataframe_id, new_meta.feature_columns_types)
        return await self.repository.set_pipeline(
            dataframe_id, new_meta.pipeline)

    async def apply_changing_methods(
            self, dataframe_id: PydanticObjectId,
            method_params: List[schemas.ApplyMethodParams],
            new_filename: str = None) -> DataFrameMetadata:
        await self.dataframe_service._ensure_not_prediction(dataframe_id)
        await self.dataframe_service._check_filename_exists(new_filename)
        dataframe_meta, df = await self._get_df_and_meta(dataframe_id)

        new_df, new_meta = await self._apply_methods_to_df(
            df, dataframe_meta, method_params)

        return await self.dataframe_service.save_transformed_dataframe(
            changed_df_meta=new_meta, new_df=new_df, new_filename=new_filename)

    async def _apply_methods_to_df(
            self,
            df: pd.DataFrame,
            dataframe_meta: DataFrameMetadata,
            method_params: List[schemas.ApplyMethodParams]
    ) -> (pd.DataFrame, DataFrameMetadata):
        methods_applier = MethodsApplier(df, dataframe_meta)
        for method_params in method_params:
            methods_applier.apply_method(method_params=method_params)
        return methods_applier.get_df(), methods_applier.get_meta()

    async def copy_pipeline(self, id_from: PydanticObjectId,
                            id_to: PydanticObjectId,
                            new_filename: str) -> DataFrameMetadata:
        await self.dataframe_service._check_filename_exists(new_filename)
        new_df, new_meta = await self._copy_pipeline_common(id_from, id_to)
        return await self.dataframe_service.save_transformed_dataframe(
            changed_df_meta=new_meta, new_df=new_df, new_filename=new_filename)

    async def copy_pipeline_for_prediction(self, id_from: PydanticObjectId,
                            id_to: PydanticObjectId) -> pd.DataFrame:
        new_df, new_meta = await self._copy_pipeline_common(id_from, id_to)
        return new_df

    async def _copy_pipeline_common(self, id_from, id_to):
        await self.dataframe_service._ensure_not_prediction(id_from)
        await self.dataframe_service._ensure_not_prediction(id_to)
        pipeline_from_source_df = await self.repository.get_pipeline(id_from)
        dataframe_meta, df = await self._get_df_and_meta(id_to)
        new_df, new_meta = await self._apply_methods_to_df(
            df, dataframe_meta, pipeline_from_source_df)
        return new_df, new_meta

from typing import List

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

    async def _ensure_not_prediction(self, dataframe_id: PydanticObjectId):
        if await self.repository.get_is_prediction(dataframe_id):
            raise errors.DataFrameIsPredictionError(dataframe_id)

    async def _get_df_and_meta(self, dataframe_id: PydanticObjectId):
        dataframe_meta = await self.repository.get_dataframe_meta(dataframe_id)
        df = await self.repository.read_pandas_dataframe(dataframe_id)
        return dataframe_meta, df

    async def process_feature_importances(
            self,
            dataframe_id: PydanticObjectId,
            task_type: specs.FeatureSelectionTaskType,
            feature_selection_params: List[schemas.SelectorMethodParams]
    ) -> schemas.FeatureSelectionSummary:
        await self._ensure_not_prediction(dataframe_id)
        features, target = await self.dataframe_service.get_feature_target_df_supervised(
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
        await self._ensure_not_prediction(dataframe_id)
        dataframe_meta, df = await self._get_df_and_meta(dataframe_id)

        new_df, new_meta = await self._apply_methods_to_df(
            df, dataframe_meta, method_params)

        await self.repository.save_pandas_dataframe(dataframe_id, new_df)
        await self.repository.set_feature_column_types(
            dataframe_id, new_meta.feature_columns_types)
        return await self.repository.set_pipeline(
            dataframe_id, new_meta.pipeline)

    async def apply_changing_methods(self, dataframe_id: PydanticObjectId,
                                     method_params: List[schemas.ApplyMethodParams]
                                     ) -> DataFrameMetadata:
        await self._ensure_not_prediction(dataframe_id)
        dataframe_meta, df = await self._get_df_and_meta(dataframe_id)

        new_df, new_meta = await self._apply_methods_to_df(
            df, dataframe_meta, method_params)

        return await self.dataframe_service.save_transformed_dataframe(
            changed_df_meta=new_meta, new_df=new_df)

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
                            id_to: PydanticObjectId) -> DataFrameMetadata:
        new_df, new_meta = await self._copy_pipeline_common(id_from, id_to)
        return await self.dataframe_service.save_transformed_dataframe(
            changed_df_meta=new_meta, new_df=new_df)

    async def copy_pipeline_for_prediction(self, id_from: PydanticObjectId,
                            id_to: PydanticObjectId) -> pd.DataFrame:
        new_df, new_meta = await self._copy_pipeline_common(id_from, id_to)
        return new_df

    async def _copy_pipeline_common(self, id_from, id_to):
        await self._ensure_not_prediction(id_from)
        await self._ensure_not_prediction(id_to)
        pipeline_from_source_df = await self.repository.get_pipeline(id_from)
        dataframe_meta, df = await self._get_df_and_meta(id_to)
        new_df, new_meta = await self._apply_methods_to_df(
            df, dataframe_meta, pipeline_from_source_df)
        return new_df, new_meta

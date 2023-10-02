from typing import List

import pandas as pd
from beanie import PydanticObjectId

from ml_api.apps.dataframes import specs, schemas, errors
from ml_api.apps.dataframes.models import DataFrameMetadata
from ml_api.apps.dataframes.repositories.repository_manager import \
    DataframeRepositoryManager
from ml_api.apps.dataframes.services.methods_applier import \
    MethodsApplier
from ml_api.apps.dataframes.services.feature_selector import \
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

    async def process_feature_importances(
            self,
            dataframe_id: PydanticObjectId,
            task_type: specs.FeatureSelectionTaskType,
            feature_selection_params: List[schemas.SelectorMethodParams]
    ) -> schemas.FeatureSelectionSummary:
        if await self.repository.get_is_prediction(dataframe_id):
            raise errors.DataFrameIsPredictionError(dataframe_id)
        features, target = await self.dataframe_service.get_feature_target_df_supervised(dataframe_id)
        selector = FeatureSelector(features, target, task_type, feature_selection_params)
        empty_summary = selector.get_empty_summary()
        await self.repository.set_feature_importance_report(dataframe_id, empty_summary)
        try:
            summary = selector.get_summary()
        except Exception as err:
            await self.repository.set_feature_importance_report(dataframe_id, None)
            raise err
        await self.repository.set_feature_importance_report(dataframe_id, summary)
        return summary

    async def apply_methods(self, dataframe_id: PydanticObjectId,
                            method_params: List[schemas.ApplyMethodParams]
                            ) -> DataFrameMetadata:
        dataframe_meta = await self.repository.get_dataframe_meta(
            dataframe_id)
        if dataframe_meta.is_prediction:
            raise errors.DataFrameIsPredictionError(dataframe_id)
        df = await self.repository.read_pandas_dataframe(dataframe_id)

        new_df, new_dataframe_meta = await self._apply_methods_to_df(
            df, dataframe_meta, method_params)

        return await self.dataframe_service.save_transformed_dataframe(
            changed_df_meta=new_dataframe_meta,
            new_df=new_df)

    async def _apply_methods_to_df(
            self,
            df: pd.DataFrame,
            dataframe_meta: DataFrameMetadata,
            method_params: List[schemas.ApplyMethodParams]
    ) -> DataFrameMetadata:
        methods_applier = MethodsApplier(df, dataframe_meta)
        for method_params in method_params:
            methods_applier.apply_method(method_params=method_params)
        new_df = methods_applier.get_df()
        new_dataframe_meta = methods_applier.get_meta()
        return new_df, new_dataframe_meta

    async def copy_pipeline(self, id_from: PydanticObjectId,
                            id_to: PydanticObjectId) -> DataFrameMetadata:
        if await self.repository.get_is_prediction(id_from):
            raise errors.DataFrameIsPredictionError(id_from)
        if await self.repository.get_is_prediction(id_to):
            raise errors.DataFrameIsPredictionError(id_to)
        pipeline_from_source_df = await self.repository.get_pipeline(id_from)
        return await self.apply_methods(id_to, pipeline_from_source_df)

    async def copy_pipeline_for_prediction(self, id_from: PydanticObjectId,
                            id_to: PydanticObjectId) -> pd.DataFrame:
        if await self.repository.get_is_prediction(id_from):
            raise errors.DataFrameIsPredictionError(id_from)
        if await self.repository.get_is_prediction(id_to):
            raise errors.DataFrameIsPredictionError(id_to)
        pipeline_from_source_df = await self.repository.get_pipeline(id_from)

        dataframe_meta = await self.repository.get_dataframe_meta(id_to)
        df = await self.repository.read_pandas_dataframe(id_to)

        new_df, new_dataframe_meta = await self._apply_methods_to_df(
            df, dataframe_meta, pipeline_from_source_df)
        return new_df

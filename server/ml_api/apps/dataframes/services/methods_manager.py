from typing import List, Any

from beanie import PydanticObjectId

from ml_api.apps.dataframes import specs
from ml_api.apps.dataframes import schemas
from ml_api.apps.dataframes.services.methods_processor import DataframeMethodProcessor
from ml_api.apps.dataframes.services.file_manager import DataframeFileManagerService
from ml_api.apps.dataframes.services.metadata_manager import DataframeMetadataManagerService
from ml_api.apps.dataframes.services.dataframe_manager import DataframeManagerService
from ml_api.apps.dataframes.services.feature_selector import FeatureSelector
from ml_api.apps.dataframes.models import DataFrameMetadata


class DataframeMethodsManagerService:
    """
    Применяет функции к датафрейму и сохраняет результаты в виде нового датафрейма.
    """
    def __init__(self, user_id):
        self._user_id = user_id
        self.file_service = DataframeFileManagerService(self._user_id)
        self.metadata_service = DataframeMetadataManagerService(self._user_id)
        self.dataframe_service = DataframeManagerService(self._user_id)

    # 4: CELERY FUNCTION OPERATIONS -------------------------------------------
    async def process_feature_importances(self, dataframe_id: PydanticObjectId,
                                          task_type: specs.FeatureSelectionTaskType,
                                          feature_selection_params: List[schemas.SelectorMethodParams]
                                          ) -> schemas.FeatureSelectionSummary:
        features, target = await self.dataframe_service.\
            get_feature_target_df_supervised(dataframe_id)
        selector = FeatureSelector(features, target, task_type, feature_selection_params)
        empty_summary = selector.get_empty_summary()
        await self.metadata_service.set_feature_importances(dataframe_id,
                                                            empty_summary)
        try:
            summary = selector.get_summary()
        except Exception:
            await self.metadata_service.set_feature_importances(dataframe_id,
                                                                None)
            return None
        await self.metadata_service.set_feature_importances(dataframe_id,
                                                            summary)
        return summary

    async def apply_methods(self, dataframe_id: PydanticObjectId,
                            method_params: List[schemas.ApplyMethodParams]
                            ) -> DataFrameMetadata:
        dataframe_meta = await self.metadata_service.get_dataframe_meta(dataframe_id)
        df = await self.file_service.read_df_from_file(dataframe_id)

        function_processor = DataframeMethodProcessor(df, dataframe_meta)
        for method_params in method_params:
            function_processor.apply_method(method_params=method_params)
        new_df = function_processor.get_df()
        new_dataframe_meta = function_processor.get_meta()
        return await self.dataframe_service.save_transformed_dataframe(
            changed_df_meta=new_dataframe_meta,
            new_df=new_df)

    async def copy_pipeline(self, id_from: PydanticObjectId,
                            id_to: PydanticObjectId) -> DataFrameMetadata:
        pipeline_from = await self.metadata_service.get_pipeline(id_from)
        return await self.apply_methods(id_to, pipeline_from)

from typing import List, Any

from beanie import PydanticObjectId

from ml_api.apps.dataframes import specs
from ml_api.apps.dataframes import schemas
from ml_api.apps.dataframes.services.methods_processor import DataframeFunctionProcessor
from ml_api.apps.dataframes.services.file_manager import DataframeFileManagerService
from ml_api.apps.dataframes.services.metadata_manager import DataframeMetadataManagerService
from ml_api.apps.dataframes.services.dataframe_manager import DataframeManagerService
from ml_api.apps.dataframes.services.feature_selector import FeatureSelector
from ml_api.apps.dataframes.models import PipelineElement


class CopyPipelineException(Exception):
    pass


class DataframeMethodsManagerService:
    def __init__(self, user_id):
        self._user_id = user_id
        self.file_service = DataframeFileManagerService(self._user_id)
        self.metadata_service = DataframeMetadataManagerService(self._user_id)
        self.dataframe_service = DataframeManagerService(self._user_id)

    # 4: CELERY FUNCTION OPERATIONS -------------------------------------------
    async def get_feature_selection_summary(self, dataframe_id: PydanticObjectId,
            feature_selection_params: List[schemas.SelectorMethodParams]
                                    ) -> schemas.FeatureSelectionSummary:
        features, target = self.dataframe_service.get_feature_target_df(dataframe_id)
        selector = FeatureSelector(features, target, feature_selection_params)
        summary = selector.get_summary()
        return summary

    async def apply_function(self, dataframe_id: PydanticObjectId,
                       function_name: specs.AvailableFunctions,
                       params: Any = None):
        # if True: return True
        df = await self.file_service.read_df_from_file(dataframe_id)
        column_types = await self.metadata_service.get_column_types(dataframe_id)

        function_processor = DataframeFunctionProcessor(df, column_types)
        function_processor.apply_function(
            function_name=function_name, params=params
        )

        new_df = function_processor.get_df()
        new_column_types = function_processor.get_column_types()
        is_pipelined = function_processor.is_pipelined_once()

        if is_pipelined:
            await self.metadata_service.add_method_to_pipeline(
                dataframe_id, function_name=function_name, params=params
            )
        await self.metadata_service.set_column_types(dataframe_id, column_types=new_column_types)
        await self.file_service.write_df_to_file(dataframe_id, new_df)

    async def copy_pipeline(self, id_from: PydanticObjectId, id_to: PydanticObjectId):
        # if True: return True
        check_pipeline = await self.metadata_service.get_pipeline(id_to)
        if len(check_pipeline) != 0:
            raise CopyPipelineException(
                f"Pipeline in document with id {id_to} already exists")
        pipeline_from = await self.metadata_service.get_pipeline(id_from)
        await self._apply_pipeline_to_csv(id_to, pipeline_from)

    async def _apply_pipeline_to_csv(self, dataframe_id: PydanticObjectId,
                               pipeline: List[PipelineElement]) -> bool:
        """Применяет либо все либо ничего"""
        column_types = await self.metadata_service.get_column_types(
            dataframe_id)
        df = await self.file_service.read_df_from_file(dataframe_id)
        function_processor = DataframeFunctionProcessor(df, column_types)
        for function in pipeline:
            function_processor.apply_function(
                function.function_name, function.params
            )

        new_column_types = function_processor.get_column_types()
        new_df = function_processor.get_df()
        new_pipeline = function_processor.get_pipeline()

        await self.metadata_service.set_pipeline(dataframe_id, new_pipeline)
        await self.metadata_service.set_column_types(dataframe_id, column_types=new_column_types)
        await self.file_service.write_df_to_file(dataframe_id, new_df)

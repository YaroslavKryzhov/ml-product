from uuid import UUID
from typing import List, Any

import ml_api.apps.dataframes.schemas as schemas
import ml_api.apps.dataframes.specs as specs
from ml_api.apps.dataframes.repository import DataFrameInfoCRUD
from ml_api.apps.dataframes.services.methods_processor import DataframeFunctionProcessor

from ml_api.apps.dataframes.services.file_manager import DataframeFileManagerService
from ml_api.apps.dataframes.services.metadata_manager import DataframeMetadataManagerService


class CopyPipelineException(Exception):
    pass


class DataframeMethodsManagerService:
    def __init__(self, db, user_id):
        self._db = db
        self._user_id = user_id
        self.info_repository = DataFrameInfoCRUD(self._db, self._user_id)
        self.file_service = DataframeFileManagerService(self._db,
                                                        self._user_id)
        self.metadata_service = DataframeMetadataManagerService(self._db,
                                                        self._user_id)

    # 4: CELERY FUNCTION OPERATIONS -------------------------------------------

    def _get_dataframe_pipeline(self, dataframe_id: UUID) -> List[
        schemas.PipelineElement]:
        return self.info_repository.get(
            dataframe_id).pipeline

    def _set_pipeline(self, dataframe_id: UUID,
                      pipeline: List[schemas.PipelineElement]):
        query = {'pipeline': pipeline}
        self.info_repository.update(dataframe_id, query)

    def _update_pipeline(self, dataframe_id: UUID,
                         function_name: specs.AvailableFunctions,
                         params: Any = None):
        pipeline = self._get_dataframe_pipeline(dataframe_id)
        pipeline.append(schemas.PipelineElement(
            function_name=function_name, params=params
        ))
        query = {'pipeline': pipeline}
        self.info_repository.update(dataframe_id, query)

    def apply_function(
            self,
            dataframe_id: UUID,
            function_name: specs.AvailableFunctions,
            params: Any = None,
    ):
        df = self.file_service.read_file_to_df(dataframe_id)
        column_types = self.metadata_service.get_dataframe_column_types(dataframe_id)

        function_processor = DataframeFunctionProcessor(df, column_types)
        function_processor.apply_function(
            function_name=function_name, params=params
        )

        new_df = function_processor.get_df()
        new_column_types = function_processor.get_column_types()
        is_pipelined = function_processor.is_pipelined_once()

        if is_pipelined:
            self._update_pipeline(
                dataframe_id, function_name=function_name, params=params
            )
        self.metadata_service.set_column_types(dataframe_id, column_types=new_column_types)
        self.file_service.save_df_to_file(dataframe_id, new_df)

    def copy_pipeline(self, id_from: UUID, id_to: UUID):
        already_exists = len(self._get_dataframe_pipeline(id_to)) != 0
        if already_exists:
            raise CopyPipelineException(
                f"Pipeline in document with id {id_to} already exists")
        pipeline = self._get_dataframe_pipeline(id_from)
        self._apply_pipeline_to_csv(id_to, pipeline)

    def _apply_pipeline_to_csv(
            self, dataframe_id: UUID, pipeline: List[schemas.PipelineElement]
    ) -> bool:
        """Everyone is ok or no one was applied"""
        df = self.file_service.read_file_to_df(dataframe_id)
        column_types = self.metadata_service.get_dataframe_column_types(dataframe_id)
        function_processor = DataframeFunctionProcessor(df, column_types)
        for function in pipeline:
            function_processor.apply_function(
                function.function_name, function.params
            )

        new_column_types = function_processor.get_column_types()
        new_df = function_processor.get_df()
        new_pipeline = function_processor.get_pipeline()

        self._set_pipeline(dataframe_id, new_pipeline)
        self.metadata_service.set_column_types(dataframe_id, column_types=new_column_types)
        self.file_service.save_df_to_file(dataframe_id, new_df)

    # -------------------------------------------------------------------------

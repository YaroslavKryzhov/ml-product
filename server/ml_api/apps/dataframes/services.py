import os
from uuid import UUID
from typing import List, Any, Union
from datetime import datetime

from fastapi.responses import FileResponse
from fastapi import HTTPException, status
import pandas as pd

import ml_api.apps.dataframes.schemas as schemas
import ml_api.apps.dataframes.specs.specs as specs
from ml_api.apps.dataframes.repository import DataFrameInfoCRUD, \
    DataFrameFileCRUD
import ml_api.apps.dataframes.utils.utils as utils
from ml_api.apps.dataframes.utils.df_worker import DataframeFunctionProcessor


class CopyPipelineException(Exception):
    pass


class DataframeManagerService:
    def __init__(self, db, user_id):
        self._db = db
        self._user_id = user_id

    # 1: FILE MANAGEMENT OPERATIONS -------------------------------------------
    def upload_file(self, file, filename: str) -> str:
        dataframe = DataFrameInfoCRUD(self._db, self._user_id).create(filename)
        DataFrameFileCRUD().upload(file_uuid=dataframe.id, file=file)
        column_types = self._define_column_types(dataframe.id)
        self._set_column_types(dataframe.id, column_types)
        return str(dataframe.id)

    def download_file(self, dataframe_id: UUID) -> FileResponse:
        dataframe_info = DataFrameInfoCRUD(self._db, self._user_id).get(
            dataframe_id)
        response = DataFrameFileCRUD().download_csv(
            file_uuid=dataframe_id, filename=dataframe_info.filename)
        return response

    def rename_file(self, dataframe_id: UUID, new_filename: str):
        query = {'filename': new_filename}
        DataFrameInfoCRUD(self._db, self._user_id).update(dataframe_id, query)

    def delete_file(self, dataframe_id: UUID):
        DataFrameInfoCRUD(self._db, self._user_id).delete(dataframe_id)
        DataFrameFileCRUD().delete(dataframe_id)

    def _read_file_to_df(self, dataframe_id: UUID) -> pd.DataFrame:
        return DataFrameFileCRUD().read_csv(dataframe_id)

    def _save_df_to_file(self, dataframe_id: UUID, df: pd.DataFrame):
        DataFrameFileCRUD().save_csv(dataframe_id=dataframe_id, data=df)

    # 2: GET OPERATIONS -------------------------------------------------------
    def get_dataframe_info(self, dataframe_id: UUID) -> schemas.DataFrameInfo:
        return DataFrameInfoCRUD(self._db, self._user_id).get(dataframe_id)

    def _get_dataframe_column_types(self,
                                    dataframe_id: UUID) -> schemas.ColumnTypes:
        return DataFrameInfoCRUD(self._db, self._user_id).get(
            dataframe_id).column_types

    def _get_dataframe_pipeline(self, dataframe_id: UUID) -> List[
        schemas.PipelineElement]:
        return DataFrameInfoCRUD(self._db, self._user_id).get(
            dataframe_id).pipeline

    def get_all_dataframes_info(self) -> List[schemas.DataFrameInfo]:
        return DataFrameInfoCRUD(self._db, self._user_id).get_all()

    def get_dataframe_statistic_description(
            self, filename: str
    ) -> schemas.DataFrameDescription:
        df = self._read_file_to_df(filename)
        return utils._get_dataframe_statistic_description_data(df)

    def get_dataframe_with_pagination(
            self, dataframe_id: UUID, page: int = 1, rows_on_page: int = 50
    ) -> schemas.ReadDataFrameResponse:
        df = self._read_file_to_df(dataframe_id)
        length = len(df)
        pages_count = (length - 1) // rows_on_page + 1
        start_index = (page - 1) * rows_on_page
        stop_index = page * rows_on_page
        if stop_index < length:
            return {
                'total': pages_count,
                'records': df.iloc[start_index:stop_index]
                .fillna("")
                .to_dict('list'),
            }
        elif start_index < length:
            return {
                'total': pages_count,
                'records': df.iloc[start_index:]
                .fillna("")
                .to_dict('list'),
            }
        else:
            return {
                'total': pages_count,
                'records': pd.DataFrame().fillna("").to_dict('list'),
            }

    def get_dataframe_columns(self, dataframe_id: UUID) -> List[str]:
        return self._read_file_to_df(dataframe_id).columns.to_list()

    def get_dataframe_column_statistics(
            self, dataframe_id: UUID, bins: int = 10
    ) -> List[schemas.ColumnDescription]:
        result = []
        df = self._read_file_to_df(dataframe_id)
        column_types = self._get_dataframe_column_types(dataframe_id)
        for column_name in column_types.numeric:
            result.append(utils._get_column_histogram_data(
                df=df, column_name=column_name, bins=bins))
        for column_name in column_types.categorical:
            result.append(utils._get_column_value_counts_data
                          (df=df, column_name=column_name))
        return result

    # 3: SET OPERATIONS -------------------------------------------------------
    def _define_column_types(self, dataframe_id: UUID) -> schemas.ColumnTypes:
        df = self._read_file_to_df(dataframe_id)
        return utils._define_column_types(df)

    def _set_column_types(self, dataframe_id: UUID,
                          column_types: schemas.ColumnTypes):
        query = {
            'column_types': column_types,
            'updated_at': str(datetime.now())
        }
        DataFrameInfoCRUD(self._db, self._user_id).update(dataframe_id, query)

    def set_target_column(self, dataframe_id: UUID, target_column: str):
        column_types = self._get_dataframe_column_types(dataframe_id)
        if (target_column in column_types.numeric or
                target_column in column_types.categorical):
            column_types.target = target_column
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Column {target_column} not found in df.columns."
            )
        self._set_column_types(dataframe_id, column_types)

    def change_column_type_to_categorical(self, dataframe_id: UUID,
                                          column_name: str):
        column_types = self._get_dataframe_column_types(dataframe_id)
        try:
            column_types.numeric.remove(column_name)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Column {column_name} not found in numeric columns."
            )
        column_types.categorical.append(column_name)
        self._set_column_types(dataframe_id, column_types)

    def change_column_type_to_numeric(self, dataframe_id: UUID,
                                      column_name: str):
        df = self._read_file_to_df(dataframe_id)
        column_types = self._get_dataframe_column_types(dataframe_id)
        try:
            column_types.categorical.remove(column_name)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Column {column_name} not found in categorical columns."
            )
        column_types.numeric.append(column_name)

        try:
            df[column_name] = pd.to_numeric(df[column_name])
            DataFrameFileCRUD().save_csv(dataframe_id, df)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Column {column_name} can't be parsed like numeric."
            )

        self._set_column_types(dataframe_id, column_types)
        return True

    def _set_pipeline(self, dataframe_id: UUID,
                      pipeline: List[schemas.PipelineElement]):
        query = {'pipeline': pipeline}
        DataFrameInfoCRUD(self._db, self._user_id).update(dataframe_id, query)

    def _update_pipeline(self, dataframe_id: UUID,
                         function_name: specs.AvailableFunctions,
                         params: Any = None):
        pipeline = self._get_dataframe_pipeline(dataframe_id)
        pipeline.append(schemas.PipelineElement(
            function_name=function_name, params=params
        ))
        query = {'pipeline': pipeline}
        DataFrameInfoCRUD(self._db, self._user_id).update(dataframe_id, query)

    # 4: CELERY FUNCTION OPERATIONS -------------------------------------------
    def apply_function(
            self,
            dataframe_id: UUID,
            function_name: str,
            params: Any = None,
    ):
        df = self._read_file_to_df(dataframe_id)
        column_types = self._get_dataframe_column_types(dataframe_id)
        function_name = specs.AvailableFunctions(function_name)

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
        self._set_column_types(dataframe_id, column_types=new_column_types)
        DataFrameFileCRUD().save_csv(dataframe_id, new_df)

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
        df = self._read_file_to_df(dataframe_id)
        column_types = self._get_dataframe_column_types(dataframe_id)
        function_processor = DataframeFunctionProcessor(df, column_types)
        for function in pipeline:
            function_processor.apply_function(
                function.function_name, function.params
            )

        new_column_types = function_processor.get_column_types()
        new_df = function_processor.get_df()
        new_pipeline = function_processor.get_pipeline()

        self._set_pipeline(dataframe_id, new_pipeline)
        self._set_column_types(dataframe_id, column_types=new_column_types)
        DataFrameFileCRUD().save_csv(dataframe_id, new_df)

    # -------------------------------------------------------------------------

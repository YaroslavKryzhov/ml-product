from uuid import UUID
from typing import List, Any
from datetime import datetime

from fastapi.responses import FileResponse
import pandas as pd

import ml_api.apps.dataframes.controller.schemas as schemas
import ml_api.apps.dataframes.specs.specs as specs
from ml_api.apps.dataframes.repository.repository import DataFrameInfoCRUD, DataFrameFileCRUD
import ml_api.apps.dataframes.service.utils as utils
from ml_api.apps.dataframes.service.function_service_RAW import DataframeFunctionService


class DataframeManagerService:
    def __init__(self, db, user_id):
        self._db = db
        self._user_id = user_id

    # 1: FILE MANAGEMENT OPERATIONS -------------------------------------------
    def upload_file(self, file, filename: str) -> bool:
        if self._check_if_dataframe_name_exists(filename):
            return False
        dataframe_id = DataFrameInfoCRUD(self._db, self._user_id).create(filename)
        DataFrameFileCRUD().upload(file_uuid=dataframe_id, file=file)
        column_types = self._define_column_types(dataframe_id)
        self._set_column_types(dataframe_id, column_types)
        return True

    def download_file(self, dataframe_id: UUID) -> FileResponse:
        dataframe_info = DataFrameInfoCRUD(self._db, self._user_id).get(dataframe_id)
        response = DataFrameFileCRUD().download_csv(
            file_uuid=dataframe_id, filename=dataframe_info.filename)
        return response

    def rename_file(self, dataframe_id: UUID, new_filename: str) -> bool:
        if self._check_if_dataframe_name_exists(new_filename):
            return False
        query = {'filename': new_filename}
        DataFrameInfoCRUD(self._db, self._user_id).update(dataframe_id, query)
        return True

    def delete_file(self, dataframe_id: UUID):
        DataFrameInfoCRUD(self._db, self._user_id).delete(dataframe_id)
        DataFrameFileCRUD().delete(dataframe_id)

    def _check_if_dataframe_name_exists(self, filename: str) -> bool:
        dataframe_info = DataFrameInfoCRUD(self._db, self._user_id).get_by_name(
            filename)
        if dataframe_info:
            return True
        else:
            return False

    def _read_file_to_df(self, dataframe_id: UUID) -> pd.DataFrame:
        return DataFrameFileCRUD().read_csv(dataframe_id)

    def _save_df_to_file(self, dataframe_id: UUID, df: pd.DataFrame):
        DataFrameFileCRUD().save_csv(dataframe_id=dataframe_id, data=df)

    # 2: GET OPERATIONS -------------------------------------------------------
    def get_dataframe_info(self, dataframe_id: UUID) -> schemas.DataFrameInfo:
        return DataFrameInfoCRUD(self._db, self._user_id).get(dataframe_id)

    def _get_dataframe_column_types(self, dataframe_id: UUID) -> schemas.ColumnTypes:
        return DataFrameInfoCRUD(self._db, self._user_id).get(dataframe_id).column_types

    def _get_dataframe_pipeline(self, dataframe_id: UUID) -> List[schemas.PipelineElement]:
        return DataFrameInfoCRUD(self._db, self._user_id).get(dataframe_id).pipeline

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

    def _set_column_types(self, dataframe_id: UUID, column_types: schemas.ColumnTypes):
        query = {
            'column_types': column_types,
            'updated_at': str(datetime.now())
        }
        DataFrameInfoCRUD(self._db, self._user_id).update(dataframe_id, query)

    def set_target_column(self, dataframe_id: UUID, target_column: str):
        column_types = self._get_dataframe_column_types(dataframe_id)
        column_types.target = target_column
        self._set_column_types(dataframe_id, column_types)

    def change_column_type_to_categorical(self, dataframe_id: UUID, column_name: str):
        column_types = self._get_dataframe_column_types(dataframe_id)
        column_types.numeric.remove(column_name)
        column_types.categorical.append(column_name)
        self._set_column_types(dataframe_id, column_types)

    def change_column_type_to_numeric(self, dataframe_id: UUID, column_name: str):
        df = self._read_file_to_df(dataframe_id)
        try:
            df[column_name] = pd.to_numeric(df[column_name])
            DataFrameFileCRUD().save_csv(dataframe_id, df)
        except ValueError:
            return False
        column_types = self._get_dataframe_column_types(dataframe_id)
        column_types.categorical.remove(column_name)
        column_types.numeric.append(column_name)
        self._set_column_types(dataframe_id, column_types)
        return True

    def _update_pipeline(self, dataframe_id: UUID, function_name: specs.AvailableFunctions, params: Any = None,):
        pipeline = self._get_dataframe_pipeline(dataframe_id)
        pipeline.append(schemas.PipelineElement(
            function_name=function_name, params=params
        ))
        query = {'pipeline': pipeline}
        DataFrameInfoCRUD(self._db, self._user_id).update(dataframe_id, query)

    def _apply_pipeline_to_csv(
        self, dataframe_id: UUID, pipeline: List[schemas.PipelineElement]
    ) -> bool:
        for function in pipeline:
            self.apply_function(
                dataframe_id=dataframe_id,
                function_name=function.function_name,
                param=function.params,
            )

    def copy_pipeline(self, id_from: UUID, id_to: UUID):
        pipeline = self._get_dataframe_pipeline(id_from)
        self._apply_pipeline_to_csv(id_to, pipeline)

    def apply_function(
        self,
        dataframe_id: UUID,
        function_name: str,
        params: Any = None,
    ) -> bool:
        # TODO: UPDATE
        df = self._read_file_to_df(dataframe_id)
        column_types = self._get_dataframe_column_types(dataframe_id)

        function_service = DataframeFunctionService(df, column_types)
        function_service.apply_function(
            function_name=function_name, params=params
        )

        errors = function_service.get_errors()
        if len(errors) > 0:
            return False
        if function_service.is_pipelined():
            self._update_pipeline(
                dataframe_id, function_name=function_name, params=params
            )
        self._set_column_types(
            dataframe_id, column_types=function_service.get_column_types()
        )
        DataFrameFileCRUD().save_csv(
            dataframe_id, function_service.get_df()
        )
        return True

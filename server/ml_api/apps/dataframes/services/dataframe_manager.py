from beanie import PydanticObjectId
import pandas as pd

from ml_api.apps.dataframes.services.file_manager import DataframeFileManagerService
from ml_api.apps.dataframes.services.metadata_manager import DataframeMetadataManagerService
from ml_api.apps.dataframes.models import ColumnTypes, DataFrameMetadata
from ml_api.apps.dataframes import utils, specs, models
from ml_api.apps.dataframes import errors


class DataframeManagerService:
    """
    Работает с pd.Dataframe и отвечает за обработку и изменение данных внутри pandas-датафреймов.
    """
    def __init__(self, user_id):
        self._user_id = user_id
        self.metadata_service = DataframeMetadataManagerService(self._user_id)
        self.file_service = DataframeFileManagerService(self._user_id)

    # 2: GET OPERATIONS -------------------------------------------------------
    async def add_new_dataframe(self, file, filename: str) -> DataFrameMetadata:
        dataframe_meta = await self.file_service.upload_file(file, filename)
        dataframe_meta_updated = await self._define_and_set_initial_column_types(dataframe_meta.id)
        return dataframe_meta_updated

    async def save_transformed_dataframe(self, parent_id: PydanticObjectId,
                                         method_name: str, df: pd.DataFrame) -> DataFrameMetadata:
        # TODO: set new pipeline
        filename = await self.metadata_service.get_filename(parent_id)
        try:
            new_meta = await self.file_service.create_file(df,
                filename=f"{filename}_{method_name}", parent_id=parent_id)
        except errors.FilenameExistsUserError:
            new_meta = await self.file_service.create_file(df,
                filename=f"{filename}_{method_name}{utils.get_random_number()}",
                parent_id=parent_id)
        return new_meta

    async def move_dataframe_to_root(self, dataframe_id: PydanticObjectId):
        parent_id = await self.metadata_service.get_parent_id(dataframe_id)
        if parent_id is None:
            raise errors.NoParentIDError()
        await self.metadata_service.set_parent_id(dataframe_id, None)

    async def _define_and_set_initial_column_types(self, dataframe_id: PydanticObjectId) -> ColumnTypes:
        df = await self.file_service.read_df_from_file(dataframe_id)
        df = df.convert_dtypes()
        numeric_columns = df.select_dtypes(include=["integer", "floating"]).columns.to_list()
        categorical_columns = df.select_dtypes(include=["string", "boolean", "category"]).columns.to_list()
        column_types = models.ColumnTypes(numeric=numeric_columns, categorical=categorical_columns)
        await self.file_service.write_df_to_file(dataframe_id, df)
        return await self.metadata_service.set_column_types(dataframe_id, column_types)

    async def convert_column_to_new_type(self, dataframe_id: PydanticObjectId,
                                         column_name: str, new_type: specs.ColumnType):
        column_types = await self.metadata_service.get_column_types(dataframe_id)
        new_type = new_type.value

        current_type = "numeric" if new_type == "numeric" else "categorical"
        if column_name not in getattr(column_types, current_type):
            raise errors.ColumnNotFoundMetadataError(column_name, current_type)

        getattr(column_types, current_type).remove(column_name)
        getattr(column_types, new_type).append(column_name)

        df = await self.file_service.read_df_from_file(dataframe_id)
        try:
            if new_type == "categorical":
                converted_column = utils._convert_column_to_categorical(
                    df[column_name])
                if converted_column.nunique() > 1000:
                    raise errors.ColumnCantBeParsedError(column_name, "categorical",
                                                  "too many unique values")
            else:  # new_type == "numeric"
                converted_column = utils._convert_column_to_numeric(
                    df[column_name])
        except ValueError:
            raise errors.ColumnCantBeParsedError(column_name, new_type, "invalid values")

        df[column_name] = converted_column
        df = df.convert_dtypes()
        await self.file_service.write_df_to_file(dataframe_id, df)
        return await self.metadata_service.set_column_types(dataframe_id,
                                                            column_types)

    async def get_feature_df(self, dataframe_id: PydanticObjectId):
        # Todo: Странная логика обработки target
        feature_columns, target_column = await self.metadata_service.get_feature_target_column_names(
            dataframe_id=dataframe_id)
        df = await self.file_service.read_df_from_file(dataframe_id)

        if sorted(df.columns.tolist()) != sorted(feature_columns):
            raise errors.ColumnsNotEqualError(dataframe_id)
        return df

    async def get_feature_target_df(self, dataframe_id: PydanticObjectId):
        # TODO: check column_types: numeric only
        feature_columns, target_column = await self.metadata_service.get_feature_target_column_names(
            dataframe_id=dataframe_id)
        df = await self.file_service.read_df_from_file(dataframe_id)

        if target_column is None:
            raise errors.TargetNotFoundError(dataframe_id)
        features = df.drop(target_column, axis=1)
        target = df[target_column]
        if sorted(df.columns.tolist()) != sorted(feature_columns):
            raise errors.ColumnsNotEqualError(dataframe_id)
        return features, target

from typing import List, Dict

from bunnet import PydanticObjectId
import pandas as pd

from ml_api.apps.dataframes.repositories.repository_manager import \
    DataframeRepositoryManager
from ml_api.apps.dataframes.model import DataFrameMetadata
from ml_api.apps.dataframes import utils, schemas, errors
from ml_api.apps.ml_models.facade import ModelServiceFacade


class DataframeService:
    """
    Работает с pd.Dataframe и отвечает за обработку и изменение данных внутри pandas-датафреймов.
    """

    def __init__(self, user_id):
        self._user_id = user_id
        self.repository = DataframeRepositoryManager(self._user_id)
        self.models_service = ModelServiceFacade(self._user_id)

    def _define_initial_column_types(self, dataframe_id: PydanticObjectId
                                           ) -> schemas.ColumnTypes:
        df = self.repository.read_pandas_dataframe(dataframe_id)
        df, column_types = utils.convert_dtypes(df)
        self.repository.save_pandas_dataframe(dataframe_id, df)
        return self.repository.set_feature_column_types(
            dataframe_id, column_types)

    def _check_filename_exists(self, filename: str):
        existing_document = self.repository.get_by_filename(filename)
        if existing_document is not None:
            raise errors.FilenameExistsUserError(filename)

    def _check_for_target_feature(self, dataframe_id: PydanticObjectId):
        meta = self.repository.get_dataframe_meta(dataframe_id)
        if meta.target_feature is None:
            raise errors.TargetNotFoundError(dataframe_id)

    def _ensure_not_prediction(self, dataframe_id: PydanticObjectId):
        if self.repository.get_is_prediction(dataframe_id):
            raise errors.DataFrameIsPredictionError(dataframe_id)

    # 1: CREATE OPERATIONS ----------------------------------------------------
    def upload_new_dataframe(self, file,
                                   filename: str) -> DataFrameMetadata:
        self._check_filename_exists(filename)
        dataframe_meta = self.repository.upload_dataframe(file, filename)
        return self._define_initial_column_types(dataframe_meta.id)

    def save_transformed_dataframe(
            self, changed_df_meta: DataFrameMetadata,
            new_df: pd.DataFrame, new_filename: str) -> DataFrameMetadata:
        self._check_filename_exists(new_filename)
        changed_df_meta.parent_id = changed_df_meta.id
        changed_df_meta.filename = new_filename
        meta_created = self.repository.save_as_new_dataframe(
            new_df, changed_df_meta)
        return meta_created

    # 2: GET OPERATIONS -------------------------------------------------------
    def download_dataframe(self, dataframe_id):
        return self.repository.download_dataframe(dataframe_id)

    def get_dataframe_meta(self, dataframe_id) -> DataFrameMetadata:
        return self.repository.get_dataframe_meta(dataframe_id)

    def get_active_dataframes_meta(self) -> List[DataFrameMetadata]:
        return self.repository.get_active_dataframes_meta()

    def get_dataframes_trees(self) -> List[schemas.DataFrameNode]:
        dataframes = self.get_active_dataframes_meta()
        # Словарь для хранения узлов по их ID
        nodes = {str(df.id): schemas.DataFrameNode(
                id=str(df.id), filename=df.filename) for df in dataframes}

        roots = []

        for df in dataframes:
            node = nodes[str(df.id)]
            if df.parent_id is None or str(df.parent_id) not in nodes:
                # Если у узла нет родителя, то он корневой
                roots.append(node)
            else:
                # Иначе добавляем узел к его родителю
                parent_node = nodes[str(df.parent_id)]
                parent_node.children.append(node)

        return roots

    def get_feature_column_types(self, dataframe_id):
        return self.repository.get_feature_column_types(dataframe_id)

    def get_dataframe_with_pagination(self, dataframe_id: PydanticObjectId,
             page: int = 1, rows_on_page: int = 50) -> schemas.ReadDataFrameResponse:
        df = self.repository.read_pandas_dataframe(dataframe_id)
        return utils._get_dataframe_with_pagination(df, page, rows_on_page)

    def get_dataframe_column_statistics(self, dataframe_id: PydanticObjectId,
            bins: int = 10) -> List[schemas.ColumnDescription]:
        result = []
        df = self.repository.read_pandas_dataframe(dataframe_id)
        column_types = self.repository.get_feature_column_types(dataframe_id)
        for column_name in column_types.numeric:
            result.append(utils._get_numeric_column_statistics(
                df=df, column_name=column_name, bins=bins))
        for column_name in column_types.categorical:
            result.append(utils._get_categorical_column_statistics
                          (df=df, column_name=column_name))
        return result

    def get_correlation_matrix(self, dataframe_id: PydanticObjectId
                                     ) -> Dict[str, Dict[str, float]]:
        df = self.repository.read_pandas_dataframe(dataframe_id)
        return df.corr().to_dict()

    # 3: UPDATE OPERATIONS ----------------------------------------------------
    def set_filename(self, dataframe_id: PydanticObjectId,
                           new_filename: str):
        self._check_filename_exists(new_filename)
        return self.repository.set_filename(dataframe_id, new_filename)

    def set_target_feature(self, dataframe_id: PydanticObjectId,
                                 target_feature: str) -> DataFrameMetadata:
        column_types = self.repository.get_feature_column_types(
            dataframe_id)
        if not (target_feature in column_types.numeric or
                target_feature in column_types.categorical):
            raise errors.SetTargetNotFoundInMetadataError(
                dataframe_id, target_feature)
        return self.repository.set_target_feature(dataframe_id,
                                                        target_feature)

    def unset_target_feature(self, dataframe_id: PydanticObjectId
                                   ) -> DataFrameMetadata:
        target_feature = self.repository.get_target_feature(dataframe_id)
        if target_feature is None:
            raise errors.UnsetTargetFeatureError(dataframe_id)
        return self.repository.set_target_feature(dataframe_id, None)

    def move_dataframe_to_root(self, dataframe_id: PydanticObjectId,
                                     new_filename: str) -> DataFrameMetadata:
        self._check_filename_exists(new_filename)
        dataframe_meta = self.repository.get_dataframe_meta(dataframe_id)
        if dataframe_meta.is_prediction:
            raise errors.DataFrameIsPredictionError(dataframe_id)
        if dataframe_meta.parent_id is None:
            raise errors.DataFrameAlreadyRootError(dataframe_id)
        self.repository.set_filename(dataframe_id, new_filename)
        dataframe_meta = self.repository.set_parent_id(dataframe_id, None)
        return dataframe_meta

    def move_prediction_to_active(
            self, model_id: PydanticObjectId, dataframe_id: PydanticObjectId,
            new_filename: str) -> DataFrameMetadata:
        self._check_filename_exists(new_filename)
        dataframe_meta = self.repository.get_dataframe_meta(dataframe_id)
        if not dataframe_meta.is_prediction:
            raise errors.DataFrameIsNotPredictionError(dataframe_id)
        self.repository.set_filename(dataframe_id, new_filename)
        self.models_service.remove_from_model_predictions(
            model_id, dataframe_id)
        dataframe_meta = self.repository.set_is_prediction(
            dataframe_id, False)
        return self._define_initial_column_types(dataframe_meta.id)

    # 4: DELETE OPERATIONS ----------------------------------------------------
    def delete_dataframe(self, dataframe_id: PydanticObjectId
                               ) -> DataFrameMetadata:
        dataframe_meta = self.repository.get_dataframe_meta(dataframe_id)
        if dataframe_meta.is_prediction:
            raise errors.DataFrameIsPredictionError(dataframe_id)
        child_dataframes = self.repository.get_dataframe_metas_by_parent_id(
            dataframe_id)
        for child_dataframe in child_dataframes:
            self.delete_dataframe(child_dataframe.id)
        self.models_service.delete_models_by_dataframe(dataframe_id)
        dataframe_meta = self.repository.delete_dataframe(dataframe_id)
        return dataframe_meta

    def delete_prediction(self, model_id: PydanticObjectId,
                                prediction_id: PydanticObjectId
                                ) -> DataFrameMetadata:
        dataframe_meta = self.repository.get_dataframe_meta(prediction_id)
        if not dataframe_meta.is_prediction:
            raise errors.DataFrameIsNotPredictionError(prediction_id)
        self.models_service.remove_from_model_predictions(
            model_id, prediction_id)
        dataframe_meta = self.repository.delete_dataframe(prediction_id)
        return dataframe_meta

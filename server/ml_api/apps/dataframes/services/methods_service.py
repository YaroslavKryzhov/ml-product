from typing import List, Optional

import pandas as pd
from bunnet import PydanticObjectId

from ml_api.apps.dataframes import specs, schemas, errors
from ml_api.apps.dataframes.model import DataFrameMetadata
from ml_api.apps.dataframes.repositories.repository_manager import \
    DataframeRepositoryManager
from ml_api.apps.dataframes.services.processors.methods_applier import \
    MethodsApplier, MethodsApplierValidator
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

    def _get_df_and_meta(self, dataframe_id: PydanticObjectId):
        dataframe_meta = self.repository.get_dataframe_meta(dataframe_id)
        df = self.repository.read_pandas_dataframe(dataframe_id)
        columns_list = dataframe_meta.feature_columns_types.numeric + \
                       dataframe_meta.feature_columns_types.categorical
        self._check_columns_consistency(df, columns_list)
        return dataframe_meta, df

    def get_feature_target_column_names(self,
                                        dataframe_id: PydanticObjectId
                                        ) -> (List[str], Optional[str]):
        """Returns list of feature columns and target column name.
        If target column is not set, returns None instead of target column name.
        If feature columns contain categorical column, raises ColumnNotNumericError."""
        dataframe_meta = self.repository.get_dataframe_meta(dataframe_id)
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
        if len(column_types.categorical) == 0 and len(
                column_types.numeric) == 0:
            raise errors.ColumnTypesNotDefinedCriticalError(dataframe_id)
        return column_types.numeric, target_column

    def get_feature_target_df_supervised(self,
                                         dataframe_id: PydanticObjectId
                                         ) -> (pd.DataFrame, pd.Series):
        self.dataframe_service._check_for_target_feature(dataframe_id)
        features, target = self.get_feature_target_df(dataframe_id)
        if target is None:
            raise errors.TargetNotFoundSupervisedLearningCRITICALError(
                dataframe_id)
        return features, target

    def get_feature_target_df(self, dataframe_id: PydanticObjectId
                              ) -> (pd.DataFrame, Optional[pd.Series]):
        feature_columns, target_column = self.get_feature_target_column_names(
            dataframe_id=dataframe_id)
        df = self.repository.read_pandas_dataframe(dataframe_id)
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

    def _process_feature_importances(
            self,
            dataframe_id: PydanticObjectId,
            task_type: specs.FeatureSelectionTaskType,
            validated_params: List[schemas.SelectorMethodParams]
    ) -> schemas.FeatureSelectionSummary:
        features, target = self.get_feature_target_df_supervised(
            dataframe_id)
        selector = FeatureSelector(
            features, target, task_type, validated_params)
        self.repository.set_feature_importance_report(
            dataframe_id, selector.get_empty_summary())
        try:
            summary = selector.get_summary()
            self.repository.set_feature_importance_report(
                dataframe_id, summary)
            return summary
        except Exception:
            self.repository.set_feature_importance_report(
                dataframe_id, None)
            raise

    def change_columns_type(self, dataframe_id: PydanticObjectId,
                            method_params: List[
                                schemas.ApplyMethodParams]
                            ) -> DataFrameMetadata:
        self.dataframe_service._ensure_not_prediction(dataframe_id)
        validated_params = MethodsApplierValidator().validate_params(
            method_params)

        new_df, new_meta = self._apply_methods_to_df(
            dataframe_id, validated_params)

        self.repository.save_pandas_dataframe(dataframe_id, new_df)
        self.repository.set_feature_column_types(
            dataframe_id, new_meta.feature_columns_types)
        return self.repository.set_pipeline(
            dataframe_id, new_meta.pipeline)

    def delete_column(self, dataframe_id: PydanticObjectId,
                      method_params: List[
                          schemas.ApplyMethodParams],
                      new_filename: str = None
                      ) -> DataFrameMetadata:
        self.dataframe_service._ensure_not_prediction(dataframe_id)
        validated_params = MethodsApplierValidator().validate_params(
            method_params)
        return self._process_changing_methods(
            dataframe_id, validated_params, new_filename)

    def _process_changing_methods(
            self,
            dataframe_id: PydanticObjectId,
            validated_params: List[schemas.ApplyMethodParams],
            new_filename: str = None) -> DataFrameMetadata:
        new_df, new_meta = self._apply_methods_to_df(
            dataframe_id, validated_params)
        return self.dataframe_service.save_transformed_dataframe(
            changed_df_meta=new_meta, new_df=new_df, new_filename=new_filename)

    def copy_pipeline_for_prediction(self, id_from: PydanticObjectId,
                                     id_to: PydanticObjectId) -> pd.DataFrame:
        self.dataframe_service._ensure_not_prediction(id_from)
        self.dataframe_service._ensure_not_prediction(id_to)
        pipeline_from_source_df = self.repository.get_pipeline(id_from)
        validated_params = MethodsApplierValidator().validate_params(
            pipeline_from_source_df)
        new_df, _ = self._apply_methods_to_df(
            id_to, validated_params)
        return new_df

    def _apply_methods_to_df(
            self,
            dataframe_id: PydanticObjectId,
            validated_params: List[schemas.ApplyMethodParams]
    ) -> (pd.DataFrame, DataFrameMetadata):
        dataframe_meta, df = self._get_df_and_meta(dataframe_id)
        methods_applier = MethodsApplier(df, dataframe_meta, validated_params)
        methods_applier.apply_methods()
        return methods_applier.get_df(), methods_applier.get_meta()

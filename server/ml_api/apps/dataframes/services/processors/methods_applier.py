from typing import List, Any, Callable, Dict, Optional

import pandas as pd
import numpy as np
from pydantic import ValidationError
from sklearn import impute, preprocessing
from sklearn.experimental import enable_iterative_imputer  # noqa

from ml_api.apps.dataframes import model, schemas, specs, errors
from ml_api.apps.dataframes.specs import AvailableMethods as Methods


class MethodsApplierValidator:
    """
    Класс, отвечающий за применение методов.
    """

    def __init__(self):
        self._methods_list = [method for method in Methods]
        self._params_map: Dict[Methods, Callable] = {
            Methods.CHANGE_COLUMNS_TYPE: schemas.ChangeColumnsTypeParams,
            Methods.FILL_CUSTOM_VALUE: schemas.FillCustomValueParams,
            Methods.LEAVE_N_VALUES_ENCODING: schemas.LeaveNValuesParams,
            Methods.ONE_HOT_ENCODING: schemas.OneHotEncoderParams,
            Methods.ORDINAL_ENCODING: schemas.OrdinalEncodingParams,
            Methods.STANDARD_SCALER: schemas.StandardScalerParams,
            Methods.MIN_MAX_SCALER: schemas.MinMaxScalerParams,
            Methods.ROBUST_SCALER: schemas.RobustScalerParams,
        }
        self._current_method_name: Methods = None

    def _validate_params(self, method_name: Methods,
                         params: Optional[Dict[str, Any]]):
        if params is None or params == {}:
            if method_name == Methods.FILL_CUSTOM_VALUE:
                err_desc = "Parameter 'value' is required"
                raise errors.InvalidMethodParamsError(method_name.value, err_desc)
            elif method_name == Methods.LEAVE_N_VALUES_ENCODING:
                err_desc = "Parameter 'values_to_keep' is required"
                raise errors.InvalidMethodParamsError(method_name.value, err_desc)
            else:
                return None
        if method_name in self._params_map:
            schema = self._params_map[method_name]
            try:
                return schema(**params)
            except ValidationError as e:
                raise errors.InvalidMethodParamsError(method_name.value, str(e))
        else:
            return None

    def validate_params(self, methods_params: List[schemas.ApplyMethodParams]):
        validated_params = []
        for method_param in methods_params:
            method_name = method_param.method_name
            columns = method_param.columns
            params = method_param.params
            if method_name not in self._methods_list:
                raise errors.ApplyingMethodNotExistsError(method_name.value)
            self._current_method_name = method_name
            params = self._validate_params(method_name, params)
            validated_params.append(schemas.ApplyMethodParams(
                method_name=method_name, columns=columns, params=params))
        return validated_params


class MethodsApplier:
    """
    Класс, отвечающий за применение методов.
    """

    def __init__(self, 
                 df: pd.DataFrame,
                 dataframe_meta: model.DataFrameMetadata,
                 methods_params: List[schemas.ApplyMethodParams]):
        self._df: pd.DataFrame = df
        self._meta: model.DataFrameMetadata = dataframe_meta
        self.params = methods_params
        self._methods_map: Dict[Methods, Callable] = {
            Methods.DROP_DUPLICATES: self._drop_duplicates,
            Methods.DROP_COLUMNS: self._drop_columns,
            Methods.DROP_NA: self._drop_na,
            Methods.CHANGE_COLUMNS_TYPE: self._change_columns_type,
            Methods.FILL_MEAN: self._fill_mean,
            Methods.FILL_MEDIAN: self._fill_median,
            Methods.FILL_MOST_FREQUENT: self._fill_most_frequent,
            Methods.FILL_CUSTOM_VALUE: self._fill_custom_value,
            Methods.FILL_BFILL: self._fill_bfill,
            Methods.FILL_FFILL: self._fill_ffill,
            Methods.FILL_INTERPOLATION: self._fill_interpolation,
            Methods.FILL_LINEAR_IMPUTER: self._fill_linear_imputer,
            Methods.FILL_KNN_IMPUTER: self._fill_knn_imputer,
            Methods.LEAVE_N_VALUES_ENCODING: self._leave_n_values_encoding,
            Methods.ONE_HOT_ENCODING: self._one_hot_encoding,
            Methods.ORDINAL_ENCODING: self._ordinal_encoding,
            Methods.STANDARD_SCALER: self._standard_scaler,
            Methods.MIN_MAX_SCALER: self._min_max_scaler,
            Methods.ROBUST_SCALER: self._robust_scaler,
        }
        self._params_map: Dict[Methods, Callable] = {
            Methods.CHANGE_COLUMNS_TYPE: schemas.ChangeColumnsTypeParams,
            Methods.FILL_CUSTOM_VALUE: schemas.FillCustomValueParams,
            Methods.LEAVE_N_VALUES_ENCODING: schemas.LeaveNValuesParams,
            Methods.ONE_HOT_ENCODING: schemas.OneHotEncoderParams,
            Methods.ORDINAL_ENCODING: schemas.OrdinalEncodingParams,
            Methods.STANDARD_SCALER: schemas.StandardScalerParams,
            Methods.MIN_MAX_SCALER: schemas.MinMaxScalerParams,
            Methods.ROBUST_SCALER: schemas.RobustScalerParams,
        }
        self._current_method_name: Methods = None
        self._validate_column_list()

    def _validate_column_list(self):
        columns_list = self._get_column_list()
        df_columns_list = self._df.columns.tolist()
        if sorted(df_columns_list) != sorted(columns_list):
            raise errors.ColumnsNotEqualCriticalError(df_columns_list,
                                                      columns_list)

    def _validate_selected_columns(self, method_columns: List[str]):
        column_list = set(self._get_column_list())
        df_columns = self._df.columns
        for column in method_columns:
            if column not in column_list:
                raise errors.ColumnNotFoundInMetadataError(
                    column, self._current_method_name.value)
            if column not in df_columns:
                raise errors.ColumnNotFoundInDataFrameError(
                    column, self._current_method_name.value)

    def apply_methods(self):
        for method_param in self.params:
            method_name = method_param.method_name
            method_columns = method_param.columns
            params = method_param.params
            # if method_name not in self._methods_map:
            #     raise errors.ApplyingMethodNotExistsError(method_name.value)
            params = self._validate_params(method_name, params)
            self._current_method_name = method_name
            self._validate_selected_columns(method_columns)
            try:
                final_params = self._methods_map[method_name](
                    method_columns, params)
            except Exception as err:
                # print(traceback.format_exc())
                error_type = type(err).__name__
                error_description = str(err)
                raise errors.ApplyingMethodError(
                    method_name.value, f"{error_type}: {error_description}")
            self._meta.pipeline.append(
                schemas.ApplyMethodParams(
                    method_name=method_name,
                    columns=method_columns,
                    params=final_params.dict() if final_params is not None else None
                )
            )

    def _validate_params(self, method_name: Methods,
                         params: Optional[Dict[str, Any]]):
        if params is None or params == {}:
            if method_name == Methods.FILL_CUSTOM_VALUE:
                err_desc = "Parameter 'value' is required"
                raise errors.InvalidMethodParamsError(method_name.value, err_desc)
            elif method_name == Methods.LEAVE_N_VALUES_ENCODING:
                err_desc = "Parameter 'values_to_keep' is required"
                raise errors.InvalidMethodParamsError(method_name.value, err_desc)
            else:
                return None
        if method_name in self._params_map:
            schema = self._params_map[method_name]
            try:
                return schema(**params)
            except ValidationError as e:
                raise errors.InvalidMethodParamsError(method_name.value, str(e))
        else:
            return None

    def get_df(self) -> pd.DataFrame:
        return self._df

    def get_meta(self) -> model.DataFrameMetadata:
        return self._meta

    def _get_column_types(self) -> schemas.ColumnTypes:
        return self._meta.feature_columns_types

    def _set_column_types(self, column_types: schemas.ColumnTypes):
        self._meta.feature_columns_types = column_types

    def _remove_columns_from_column_types(self,
                                          column_types: schemas.ColumnTypes,
                                          columns: List[str]):
        for column in columns:
            if column in column_types.numeric:
                column_types.numeric.remove(column)
            elif column in column_types.categorical:
                column_types.categorical.remove(column)
            else:
                raise errors.ColumnNotFoundInMetadataCriticalError(
                    column, self._current_method_name.value)

    def _get_target_feature(self) -> schemas.ColumnTypes:
        return self._meta.target_feature

    def _get_column_list(self) -> List[str]:
        column_types = self._get_column_types()
        return column_types.numeric + column_types.categorical

    def _check_for_numeric_type(self, columns: List[str]):
        column_types = self._get_column_types()
        for column in columns:
            if column not in column_types.numeric:
                raise errors.ColumnNotNumericError(
                    column, self._current_method_name.value)

    def _check_for_categorical_type(self, columns: List[str]):
        column_types = self._get_column_types()
        for column in columns:
            if column not in column_types.categorical:
                raise errors.ColumnNotCategoricalError(
                    column, self._current_method_name.value)

    def _check_for_target_feature(self, columns: List[str]):
        target_feature = self._get_target_feature()
        if target_feature in columns:
            raise errors.ColumnIsTargetFeatureError(
                target_feature, self._current_method_name.value)

    def _check_for_nans(self, columns: List[str]):
        columns_with_nan = [column for column in columns if
                            self._df[column].isna().sum() > 0]
        if columns_with_nan:
            raise errors.NansInDataFrameError(', '.join(columns_with_nan),
                                              self._current_method_name.value)

    def _drop_columns(self, columns: List[str], params: Dict[str, Any]):
        self._check_for_target_feature(columns)
        self._df.drop(columns, axis=1, inplace=True)
        column_types = self._get_column_types()
        self._remove_columns_from_column_types(column_types, columns)
        self._set_column_types(column_types)

    def _change_columns_type(self, columns: List[str],
                             params: schemas.ChangeColumnsTypeParams):
        new_type = params.new_type
        column_types = self._get_column_types()
        if new_type == specs.ColumnType.NUMERIC:
            # self._check_for_categorical_type(columns)
            self._remove_columns_from_column_types(column_types, columns)
            self._convert_columns_to_numeric(columns)
            column_types.numeric.extend(columns)
        elif new_type == specs.ColumnType.CATEGORICAL:
            # self._check_for_numeric_type(columns)
            self._remove_columns_from_column_types(column_types, columns)
            self._convert_columns_to_categorical(columns)
            column_types.categorical.extend(columns)
        self._set_column_types(column_types)
        return params

    def _convert_columns_to_categorical(self, columns: List[str]):
        for column_name in columns:
            try:
                converted_column = self._df[column_name].astype(str)
            except ValueError as err:
                raise errors.ChangeColumnTypeError(
                    column_name, specs.ColumnType.CATEGORICAL.value, str(err))
            nunique = converted_column.nunique()
            if nunique > 1000:
                err_desc = f"Column has too many (>1000) unique values: {nunique}"
                raise errors.ChangeColumnTypeError(
                    column_name, specs.ColumnType.CATEGORICAL.value, err_desc)
            self._df[column_name] = converted_column

    def _convert_columns_to_numeric(self, columns: List[str]):
        for column_name in columns:
            try:
                self._df[column_name] = pd.to_numeric(self._df[column_name])
            except ValueError as err:
                raise errors.ChangeColumnTypeError(
                    column_name, specs.ColumnType.NUMERIC.value, str(err))

    # PART 1: MISSING DATA AND DUPLICATES--------------------------------------
    def _drop_duplicates(self, columns: List[str], params: Optional = None):
        self._df.drop_duplicates(inplace=True)

    def _drop_na(self, columns: List[str], params: Optional = None):
        self._df.dropna(subset=columns, inplace=True)

    def _fill_mean(self, columns: List[str], params: Optional = None):
        self._check_for_numeric_type(columns)
        self._df[columns] = pd.DataFrame(
            impute.SimpleImputer(strategy='mean').fit_transform(self._df[columns]),
            self._df.index, columns)

    def _fill_median(self, columns: List[str], params: Optional = None):
        self._check_for_numeric_type(columns)
        self._df[columns] = pd.DataFrame(
            impute.SimpleImputer(strategy='median').fit_transform(self._df[columns]),
            self._df.index, columns)

    def _fill_most_frequent(self, columns: List[str], params: Optional = None):
        self._check_for_categorical_type(columns)
        self._df[columns] = pd.DataFrame(
            impute.SimpleImputer(strategy='most_frequent').fit_transform(self._df[columns]),
            self._df.index, columns)

    def _fill_custom_value(self, columns: List[str], params: schemas.FillCustomValueParams):
        for i, column in enumerate(columns):
            column_dtype = str(self._df[column].dtype)
            value = params.values_to_fill[i]
            try:
                pd.Series([value]).astype(column_dtype)
            except ValueError:
                raise errors.FillCustomValueWrongDTypeError(
                    column, column_dtype, value, type(value))
            self._df[column] = self._df[column].fillna(value)
        return params

    def _fill_bfill(self, columns: List[str], params: Optional = None):
        self._df[columns] = self._df[columns].bfill()

    def _fill_ffill(self, columns: List[str], params: Optional = None):
        self._df[columns] = self._df[columns].ffill()

    def _fill_interpolation(self, columns: List[str], params: Optional = None):
        self._check_for_numeric_type(columns)
        self._df[columns] = self._df[columns].interpolate()

    def _fill_linear_imputer(self, columns: List[str], params: Optional = None):
        self._check_for_numeric_type(columns)
        self._df[columns] = pd.DataFrame(impute.IterativeImputer(
            ).fit_transform(self._df[columns]), self._df.index, columns)

    def _fill_knn_imputer(self, columns: List[str], params: Optional = None):
        self._check_for_numeric_type(columns)
        self._df[columns] = pd.DataFrame(impute.KNNImputer().fit_transform(
                self._df[columns]), self._df.index, columns)

    # PART 2: FEATURE ENCODING ------------------------------------------------
    def _check_before_encoding(self, columns):
        self._check_for_categorical_type(columns)
        self._check_for_target_feature(columns)
        self._check_for_nans(columns)

    def _leave_n_values_encoding(self, columns: List[str],
                                 params: schemas.LeaveNValuesParams):
        """LeaveNValues encoding method. Leave only groups of values that
        are listed in params.values_to_keep"""
        self._check_before_encoding(columns)
        self._df[columns] = self._df[columns].astype('str')
        for i, column in enumerate(columns):
            self._df[column] = self._df[column].where(self._df[column].isin(
                    params.values_to_keep[i]), 'Others')
        return params

    def _one_hot_encoding(self, columns: List[str],
                          params: Optional[schemas.OneHotEncoderParams] = None):
        self._check_before_encoding(columns)
        self._df[columns] = self._df[columns].astype('str')
        encoder = preprocessing.OneHotEncoder(drop='first')
        if params is None:
            encoder.fit(self._df[columns])
            categories_ = [cat.tolist() for cat in encoder.categories_]
            drop_idx_ = encoder.drop_idx_.tolist()
            # print(encoder._drop_idx_after_grouping)
            infrequent_enabled = encoder._infrequent_enabled
            n_features_outs = encoder._n_features_outs
            params = schemas.OneHotEncoderParams(
                categories_=categories_, drop_idx_=drop_idx_,
                infrequent_enabled=infrequent_enabled,
                n_features_outs=n_features_outs)
        else:
            encoder.categories_ = [np.array(cat) for cat in params.categories_]
            encoder.drop_idx_ = np.array(params.drop_idx_)
            encoder._infrequent_enabled = params.infrequent_enabled
            encoder._n_features_outs = params.n_features_outs
        new_cols = encoder.get_feature_names_out(columns)
        self._df[new_cols] = encoder.transform(self._df[columns]).toarray().astype(int)
        self._df.drop(columns, axis=1, inplace=True)

        column_types = self._get_column_types()
        self._remove_columns_from_column_types(column_types, columns)
        column_types.numeric.extend(new_cols)
        self._set_column_types(column_types)
        return params

    def _ordinal_encoding(self, columns: List[str],
                          params: Optional[schemas.OrdinalEncodingParams] = None):
        self._check_before_encoding(columns)
        self._df[columns] = self._df[columns].astype('str')
        encoder = preprocessing.OrdinalEncoder()
        if params is None:
            encoder.fit(self._df[columns])
            categories_ = [cat.tolist() for cat in encoder.categories_]
            missing_indices = encoder._missing_indices
            params = schemas.OrdinalEncodingParams(categories_=categories_,
                missing_indices=missing_indices)
        else:
            encoder.categories_ = [np.array(cat) for cat in params.categories_]
            encoder._missing_indices = params.missing_indices
        self._df[columns] = encoder.transform(self._df[columns]).astype(int)

        column_types = self._get_column_types()
        self._remove_columns_from_column_types(column_types, columns)
        column_types.numeric.extend(columns)
        self._set_column_types(column_types)
        return params

    # PART 3: FEATURE SCALING -------------------------------------------------
    def _check_before_scaling(self, columns):
        self._check_for_numeric_type(columns)
        self._check_for_target_feature(columns)
        self._check_for_nans(columns)

    def _standard_scaler(self, columns: List[str],
                         params: Optional[schemas.StandardScalerParams]):
        self._check_before_scaling(columns)
        scaler = preprocessing.StandardScaler()
        if params is None:
            scaler.fit(self._df[columns])
            mean_ = scaler.mean_.tolist()
            scale_ = scaler.scale_.tolist()
            params = schemas.StandardScalerParams(mean_=mean_, scale_=scale_)
        else:
            scaler.mean_ = np.array(params.mean_)
            scaler.scale_ = np.array(params.scale_)
        self._df[columns] = pd.DataFrame(scaler.transform(
            self._df[columns]), self._df.index, columns)
        return params

    def _min_max_scaler(self, columns: List[str],
                        params: Optional[schemas.MinMaxScalerParams]):
        self._check_before_scaling(columns)
        scaler = preprocessing.MinMaxScaler()
        if params is None:
            scaler.fit(self._df[columns])
            scale_ = scaler.scale_.tolist()
            min_ = scaler.min_.tolist()
            params = schemas.MinMaxScalerParams(min_=min_, scale_=scale_)
        else:
            scaler.scale_ = np.array(params.scale_)
            scaler.min_ = np.array(params.min_)
        self._df[columns] = pd.DataFrame(scaler.transform(
            self._df[columns]), self._df.index, columns)
        return params

    def _robust_scaler(self, columns: List[str],
                       params: Optional[schemas.RobustScalerParams]):
        self._check_before_scaling(columns)
        scaler = preprocessing.RobustScaler()
        if params is None:
            scaler.fit(self._df[columns])
            center_ = scaler.center_.tolist()
            scale_ = scaler.scale_.tolist()
            params = schemas.RobustScalerParams(center_=center_, scale_=scale_)
        else:
            scaler.center_ = np.array(params.center_)
            scaler.scale_ = np.array(params.scale_)
        self._df[columns] = pd.DataFrame(scaler.transform(
            self._df[columns]), self._df.index, columns)
        return params


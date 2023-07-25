from typing import List, Any, Callable, Dict

import pandas as pd
from pydantic import ValidationError
from sklearn import impute, preprocessing

from ml_api.apps.dataframes import specs, models, schemas
from ml_api.apps.dataframes import errors


class DataframeMethodProcessor:
    """
    Класс, отвечающий за применение методов.
    """
    def __init__(self, df: pd.DataFrame, dataframe_meta: models.DataFrameMetadata):
        self._df: pd.DataFrame = df
        self._meta: models.DataFrameMetadata = dataframe_meta
        self._methods: Dict[specs.AvailableMethods, Callable] = {
            specs.AvailableMethods.DROP_DUPLICATES: self._drop_duplicates(),
            specs.AvailableMethods.DROP_COLUMNS: self._drop_columns(),
            specs.AvailableMethods.DROP_NA: self._drop_na(),
            specs.AvailableMethods.FILL_MEAN: self._fill_mean(),
            specs.AvailableMethods.FILL_MEDIAN: self._fill_median(),
            specs.AvailableMethods.FILL_MOST_FREQUENT: self._fill_most_frequent(),
            specs.AvailableMethods.FILL_CUSTOM_VALUE: self._fill_custom_value(),
            specs.AvailableMethods.FILL_BFILL: self._fill_bfill(),
            specs.AvailableMethods.FILL_FFILL: self._fill_ffill(),
            specs.AvailableMethods.FILL_INTERPOLATION: self._fill_interpolation(),
            specs.AvailableMethods.FILL_LINEAR_IMPUTER: self._fill_linear_imputer(),
            specs.AvailableMethods.FILL_KNN_IMPUTER: self._fill_knn_imputer(),
            specs.AvailableMethods.LEAVE_N_VALUES_ENCODING: self._leave_n_values_encoding(),
            specs.AvailableMethods.ONE_HOT_ENCODING: self._one_hot_encoding(),
            specs.AvailableMethods.ORDINAL_ENCODING: self._ordinal_encoding(),
            specs.AvailableMethods.STANDARD_SCALER: self._standard_scaler(),
            specs.AvailableMethods.MIN_MAX_SCALER: self._min_max_scaler(),
            specs.AvailableMethods.ROBUST_SCALER: self._robust_scaler(),
        }

    def apply_method(self, method_params: schemas.ApplyMethodParams):
        method_name = method_params.method_name
        if method_name not in self._methods:
            raise errors.ApplyingMethodNotExistsError(method_name)

        columns = method_params.columns
        column_list = set(self._get_column_list())
        for column in columns:
            if column not in column_list:
                raise errors.ColumnNotFoundMetadataError(column)

        self._methods[method_name](columns, method_params.params)
        self._meta.pipeline.append(method_params)

    def get_df(self) -> pd.DataFrame:
        return self._df

    def get_meta(self) -> models.DataFrameMetadata:
        return self._meta

    def _get_column_types(self) -> models.ColumnTypes:
        return self._meta.feature_columns_types

    def _set_column_types(self, column_types: models.ColumnTypes):
        self._meta.feature_columns_types = column_types

    def _get_target_feature(self) -> models.ColumnTypes:
        return self._meta.target_feature

    def _get_column_list(self) -> List[str]:
        column_types = self._get_column_types()
        return column_types.numeric + column_types.categorical

    def _check_for_numeric_type(self, columns: List[str]):
        column_types = self._get_column_types()
        for column in columns:
            if column not in column_types.numeric:
                raise errors.ColumnNotNumericError(column)

    def _check_for_categorical_type(self, columns: List[str]):
        column_types = self._get_column_types()
        for column in columns:
            if column not in column_types.categorical:
                raise errors.ColumnNotCategoricalError(column)

    def _check_for_target_feature(self, columns: List[str]):
        target_feature = self._get_target_feature()
        if target_feature in columns:
            return True

    def _check_for_nans(self, columns: List[str]) -> bool:
        return self._df[columns].isna().sum().sum() > 0

    def _drop_columns(self, columns: List[str], params: Dict[str, Any]):
        try:
            self._df.drop(columns, axis=1, inplace=True)
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])
        column_types = self._get_column_types()
        if self._check_for_target_feature(columns):
            raise errors.TargetFeatureDeletingError(self._get_target_feature())
        for column in columns:
            try:
                column_types.numeric.remove(column)
            except ValueError:
                try:
                    column_types.categorical.remove(column)
                except ValueError:
                    raise errors.ColumnNotFoundMetadataError(column)
        self._set_column_types(column_types)

    # PART 1: MISSING DATA AND DUPLICATES--------------------------------------
    def _drop_duplicates(self, columns: List[str], params: Dict[str, Any]):
        self._df.drop_duplicates(inplace=True)

    def _drop_na(self, columns: List[str], params: Dict[str, Any]):
        try:
            self._df.dropna(subset=[columns], inplace=True)
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])

    def _fill_mean(self, columns: List[str], params: Dict[str, Any]):
        self._check_for_numeric_type(columns)
        try:
            self._df[columns] = pd.DataFrame(
                impute.SimpleImputer(strategy='mean').fit_transform(
                    self._df[columns]), self._df.index, columns)
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])

    def _fill_median(self, columns: List[str], params: Dict[str, Any]):
        self._check_for_numeric_type(columns)
        try:
            self._df[columns] = pd.DataFrame(
                impute.SimpleImputer(
                    strategy='median').fit_transform(
                    self._df[columns]), self._df.index, columns)
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])

    def _fill_most_frequent(self, columns: List[str], params: Dict[str, Any]):
        self._check_for_categorical_type(columns)
        try:
            self._df[columns] = pd.DataFrame(
                impute.SimpleImputer(
                    strategy='most_frequent').fit_transform(
                    self._df[columns]), self._df.index, columns)
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])

    def _fill_custom_value(self, columns: List[str], params: Dict[str, Any]):
        try:
            params = schemas.FillCustomValueParams(**params)
        except ValidationError:
            raise errors.WrongApplyingMethodParamsError("FillCustomValue")
        for column in columns:
            try:
                column_dtype = str(self._df[column].dtype)
            except KeyError as ke:
                raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])
            try:
                pd.Series([params.value]).astype(column_dtype)
            except ValueError:
                raise errors.WrongApplyingMethodParamsErrorFull(
                    f"Invalid value type for column '{column}'. "
                    f"Cannot convert '{type(params.value)}' to '{column_dtype}'.")
            self._df[column].fillna(params.value, inplace=True)

    def _fill_bfill(self, columns: List[str], params: Dict[str, Any]):
        try:
            self._df[columns].bfill(inplace=True)
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])

    def _fill_ffill(self, columns: List[str], params: Dict[str, Any]):
        try:
            self._df[columns].ffill(inplace=True)
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])

    def _fill_interpolation(self, columns: List[str], params: Dict[str, Any]):
        self._check_for_numeric_type(columns)
        try:
            self._df[columns].interpolate(inplace=True)
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])

    def _fill_linear_imputer(self, columns: List[str], params: Dict[str, Any]):
        self._check_for_numeric_type(columns)
        try:
            self._df[columns] = pd.DataFrame(impute.IterativeImputer(
                ).fit_transform(self._df[columns]), self._df.index, columns)
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])

    def _fill_knn_imputer(self, columns: List[str], params: Dict[str, Any]):
        self._check_for_numeric_type(columns)
        try:
            self._df[columns] = pd.DataFrame(impute.KNNImputer().fit_transform(
                self._df[columns]), self._df.index, columns)
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])

    # PART 2: FEATURE ENCODING ------------------------------------------------

    def _leave_n_values_encoding(self, columns: List[str], params: Dict[str, Any]):
        """LeaveNValues encoding method. Leave only groups of values that
        are listed in params.values_to_keep. Work with only one column."""
        try:
            params = schemas.LeaveNValuesParams(**params)
        except ValidationError:
            raise errors.WrongApplyingMethodParamsError("LeaveNValues")
        if len(columns) > 1:
            raise errors.WrongApplyingMethodParamsError("LeaveNValues")
        self._check_for_categorical_type(columns)
        try:
            self._df[columns] = self._df[columns].where(self._df[columns].isin(
                params.values_to_keep), 'Others')
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])

    def _one_hot_encoding(self, columns: List[str], params: Dict[str, Any]):
        self._check_for_categorical_type(columns)
        if self._check_for_target_feature(columns):
            raise errors.TargetFeatureEncodingError(self._get_target_feature())
        if self._check_for_nans(columns):
            raise errors.NansInDataFrameError(
                "Can't process OneHotEncoding with NaN values in pd.DataFrame")
        enc = preprocessing.OneHotEncoder(drop='first')
        try:
            enc.fit(self._df[columns])
            new_cols = enc.get_feature_names_out(columns)
            self._df[new_cols] = enc.transform(self._df[columns]).toarray()
            self._df.drop(columns, axis=1, inplace=True)
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])
        column_types = self._get_column_types()
        column_types.numeric.extend(new_cols)
        for column in columns:
            try:
                column_types.categorical.remove(column)
            except ValueError:
                raise errors.ColumnNotFoundMetadataError(column)
        self._set_column_types(column_types)

    def _ordinal_encoding(self, columns: List[str], params: Dict[str, Any]):
        # dict of encoding in params
        self._check_for_categorical_type(columns)
        if self._check_for_target_feature(columns):
            raise errors.TargetFeatureEncodingError(self._get_target_feature())
        if self._check_for_nans(columns):
            raise errors.NansInDataFrameError(
                "Can't process OrdinalEncoding with NaN values in pd.DataFrame")
        try:
            encoder = preprocessing.OrdinalEncoder()
            self._df[columns] = encoder.fit_transform(self._df[columns])
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])
        column_types = self._get_column_types()
        column_types.numeric.extend(columns)
        for column in columns:
            try:
                column_types.categorical.remove(column)
            except ValueError:
                raise errors.ColumnNotFoundMetadataError(column)
        self._set_column_types(column_types)

    # PART 3: FEATURE SCALING -------------------------------------------------

    def _standard_scaler(self, columns: List[str], params: Dict[str, Any]):
        self._check_for_numeric_type(columns)
        if self._check_for_target_feature(columns):
            raise errors.TargetFeatureEncodingError(self._get_target_feature())
        if self._check_for_nans(columns):
            raise errors.NansInDataFrameError(
                "Can't process StandardScaler with NaN values in pd.DataFrame")
        try:
            scaler = preprocessing.StandardScaler()
            self._df[columns] = pd.DataFrame(scaler.fit_transform(
                self._df[columns]), self._df.index, columns)
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])

    def _min_max_scaler(self, columns: List[str], params: Dict[str, Any]):
        self._check_for_numeric_type(columns)
        if self._check_for_target_feature(columns):
            raise errors.TargetFeatureEncodingError(self._get_target_feature())
        if self._check_for_nans(columns):
            raise errors.NansInDataFrameError(
                "Can't process MinMaxScaler with NaN values in pd.DataFrame")
        try:
            scaler = preprocessing.MinMaxScaler()
            self._df[columns] = pd.DataFrame(scaler.fit_transform(
                self._df[columns]), self._df.index, columns)
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])

    def _robust_scaler(self, columns: List[str], params: Dict[str, Any]):
        self._check_for_numeric_type(columns)
        if self._check_for_target_feature(columns):
            raise errors.TargetFeatureEncodingError(self._get_target_feature())
        if self._check_for_nans(columns):
            raise errors.NansInDataFrameError(
                "Can't process RobustScaler with NaN values in pd.DataFrame")
        try:
            scaler = preprocessing.RobustScaler()
            self._df[columns] = pd.DataFrame(scaler.fit_transform(
                self._df[columns]), self._df.index, columns)
        except KeyError as ke:
            raise errors.ColumnNotFoundDataFrameError(ke.args[0][0])

    # def _outliers_isolation_forest(self, params):
    #     numeric_columns = self._column_types.numeric
    #     self._remove_target_from_columns(numeric_columns)
    #     if self._have_nans(numeric_columns):
    #         self._miss_insert_mean_mode()  # не работает на пропусках в данных
    #     outliers = ensemble.IsolationForest().fit_predict(
    #         self._df[numeric_columns])
    #     self._df = self._df.loc[outliers == 1].reset_index(drop=True)
    #
    # def _outliers_elliptic_envelope(self, params):
    #     numeric_columns = self._column_types.numeric
    #     self._remove_target_from_columns(numeric_columns)
    #     if self._have_nans(numeric_columns):
    #         self._miss_insert_mean_mode()  # не работает на пропусках в данных
    #     outliers = covariance.EllipticEnvelope().fit_predict(
    #         self._df[numeric_columns])
    #     self._df = self._df.loc[outliers == 1].reset_index(drop=True)
    #
    # def _outliers_local_factor(self, params):
    #     numeric_columns = self._column_types.numeric
    #     self._remove_target_from_columns(numeric_columns)
    #     if self._have_nans(numeric_columns):
    #         self._miss_insert_mean_mode()  # не работает на пропусках в данных
    #     outliers = neighbors.LocalOutlierFactor().fit_predict(
    #         self._df[numeric_columns])
    #     self._df = self._df.loc[outliers == 1].reset_index(drop=True)
    #
    # def _outliers_one_class_svm(self, params):
    #     numeric_columns = self._column_types.numeric
    #     self._remove_target_from_columns(numeric_columns)
    #     if self._have_nans(numeric_columns):
    #         self._miss_insert_mean_mode()  # не работает на пропусках в данных
    #     outliers = svm.OneClassSVM().fit_predict(self._df[numeric_columns])
    #     self._df = self._df.loc[outliers == 1].reset_index(drop=True)
    #
    # def _outliers_sgd_one_class_svm(self, params):
    #     numeric_columns = self._column_types.numeric
    #     self._remove_target_from_columns(numeric_columns)
    #     if self._have_nans(numeric_columns):
    #         self._miss_insert_mean_mode()  # не работает на пропусках в данных
    #     outliers = linear_model.SGDOneClassSVM().fit_predict(
    #         self._df[numeric_columns])
    #     self._df = self._df.loc[outliers == 1].reset_index(drop=True)

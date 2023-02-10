from typing import List, Any, Callable, Dict
import pandas as pd

import ml_api.apps.dataframes.controller.schemas as schemas
import ml_api.apps.dataframes.specs.specs as specs


# TODO: finish business logic of learning process
class DataframeFunctionService:
    def __init__(self, dataframe: pd.DataFrame,
                 column_types: schemas.ColumnTypes):
        self.df: pd.DataFrame = dataframe
        self.column_types: schemas.ColumnTypes = column_types
        self.update_pipeline: bool = False
        self.errors: List[str] = []
        self._functions_map: Dict[specs.AvailableFunctions, Callable] = {
            specs.AvailableFunctions.remove_duplicates: self.remove_duplicates,
            specs.AvailableFunctions.drop_na: self.drop_na,
            specs.AvailableFunctions.drop_column: self.drop_column,
            specs.AvailableFunctions.miss_insert_mean_mode: self.miss_insert_mean_mode,
            specs.AvailableFunctions.miss_linear_imputer: self.miss_linear_imputer,
            specs.AvailableFunctions.miss_knn_imputer: self.miss_knn_imputer,
            specs.AvailableFunctions.standardize_features: self.standardize_features,
            specs.AvailableFunctions.ordinal_encoding: self.ordinal_encoding,
            specs.AvailableFunctions.one_hot_encoding: self.one_hot_encoding,
            specs.AvailableFunctions.outliers_isolation_forest: self.outliers_isolation_forest,
            specs.AvailableFunctions.outliers_elliptic_envelope: self.outliers_elliptic_envelope,
            specs.AvailableFunctions.outliers_local_factor: self.outliers_local_factor,
            specs.AvailableFunctions.outliers_one_class_svm: self.outliers_one_class_svm,
            specs.AvailableFunctions.outliers_sgd_one_class_svm: self.outliers_sgd_one_class_svm,
            specs.AvailableFunctions.fs_select_percentile: self.fs_select_percentile,
            specs.AvailableFunctions.fs_select_k_best: self.fs_select_k_best,
            specs.AvailableFunctions.fs_select_fpr: self.fs_select_fpr,
            specs.AvailableFunctions.fs_select_fdr: self.fs_select_fdr,
            specs.AvailableFunctions.fs_select_fwe: self.fs_select_fwe,
            specs.AvailableFunctions.fs_select_rfe: self.fs_select_rfe,
            specs.AvailableFunctions.fs_select_from_model: self.fs_select_from_model,
            specs.AvailableFunctions.fs_select_pca: self.fs_select_pca,
        }

    def get_df(self) -> pd.DataFrame:
        return self.df

    def get_column_types(self) -> schemas.ColumnTypes:
        return self.column_types

    def get_errors(self) -> List[str]:
        return self.errors

    def is_pipelined(self) -> bool:
        return self.update_pipeline

    def no_func_error(self, params=None):
        del params
        self.errors.append('Function not found in DocumentOperator.functions_map')

    def apply_function(self, function_name: str, params: Any = None):
        func = self._functions_map.get(function_name, self.no_func_error)
        func(params)

    def check_nans(self, columns) -> bool:
        if self.df[columns].isna().sum().sum() > 0:
            return True
        return False

    def check_categorical(self) -> bool:
        if len(self.column_types.categorical) > 0:
            return True
        return False

    # CHAPTER 1: MISSING DATA AND DUPLICATES-----------------------------------

    def remove_duplicates(self):
        self.df.drop_duplicates(inplace=True)

    def drop_na(self):
        self.df.dropna(inplace=True)

    def drop_column(self, param: str):
        column = param
        self.df.drop(column, axis=1, inplace=True)
        self.update_pipeline = True
        if self.column_types:
            try:
                self.column_types.numeric.remove(column)
            except ValueError:
                try:
                    self.column_types.categorical.remove(column)
                except ValueError:
                    pass

    def miss_insert_mean_mode(self):
        numeric_columns = self.column_types.numeric
        categorical_columns = self.column_types.categorical
        self.df[numeric_columns] = pd.DataFrame(
            SimpleImputer(strategy='mean').fit_transform(
                self.df[numeric_columns]
            ),
            self.df.index,
            numeric_columns,
        )
        self.df[categorical_columns] = pd.DataFrame(
            SimpleImputer(strategy='most_frequent').fit_transform(
                self.df[categorical_columns]
            ),
            self.df.index,
            categorical_columns,
        )

    def miss_linear_imputer(self):
        numeric_columns = self.column_types.numeric
        self.df[numeric_columns] = pd.DataFrame(
            IterativeImputer().fit_transform(self.df[numeric_columns]),
            self.df.index,
            numeric_columns,
        )

    def miss_knn_imputer(self):
        numeric_columns = self.column_types.numeric
        self.df[numeric_columns] = pd.DataFrame(
            KNNImputer().fit_transform(self.df[numeric_columns]),
            self.df.index,
            numeric_columns,
        )

    # CHAPTER 2: FEATURE TRANSFORMATION----------------------------------------
    def standardize_features(self):
        numeric_columns = self.column_types.numeric
        if self.check_nans(numeric_columns):
            self.miss_insert_mean_mode()
        sc = StandardScaler()
        self.df[numeric_columns] = pd.DataFrame(
            sc.fit_transform(self.df[numeric_columns]),
            self.df.index,
            numeric_columns,
        )
        self.update_pipeline = True

    def ordinal_encoding(self):  # не работает на пропусках в данных
        categorical = self.column_types.categorical
        if self.check_nans(categorical):
            self.miss_insert_mean_mode()
        self.df[categorical] = OrdinalEncoder().fit_transform(
            self.df[categorical]
        )

        self.column_types.numeric.extend(categorical)
        self.column_types.categorical = []
        self.update_pipeline = True

    def one_hot_encoding(self):
        categorical = self.column_types.categorical
        if self.check_nans(categorical):
            self.miss_insert_mean_mode()
        enc = OneHotEncoder()
        enc.fit(self.df[categorical])
        new_cols = enc.get_feature_names(categorical)
        self.df[new_cols] = enc.transform(self.df[categorical]).toarray()
        self.df.drop(categorical, axis=1, inplace=True)

        self.column_types.numeric.extend(new_cols)
        self.column_types.categorical = []
        self.update_pipeline = True

    # CHAPTER 3: OUTLIERS------------------------------------------------------
    def outliers_isolation_forest(self):
        numeric_columns = self.column_types.numeric
        if self.check_nans(numeric_columns):
            self.miss_insert_mean_mode()
        outliers = IsolationForest().fit_predict(self.df[numeric_columns])
        self.df = self.df.loc[outliers == 1].reset_index(drop=True)

    def outliers_elliptic_envelope(self):
        numeric_columns = self.column_types.numeric
        if self.check_nans(numeric_columns):
            self.miss_insert_mean_mode()
        outliers = EllipticEnvelope().fit_predict(self.df[numeric_columns])
        self.df = self.df.loc[outliers == 1].reset_index(drop=True)

    def outliers_local_factor(self):
        numeric_columns = self.column_types.numeric
        if self.check_nans(numeric_columns):
            self.miss_insert_mean_mode()
        outliers = LocalOutlierFactor().fit_predict(self.df[numeric_columns])
        self.df = self.df.loc[outliers == 1].reset_index(drop=True)

    def outliers_one_class_svm(self):
        numeric_columns = self.column_types.numeric
        if self.check_nans(numeric_columns):
            self.miss_insert_mean_mode()
        outliers = OneClassSVM().fit_predict(self.df[numeric_columns])
        self.df = self.df.loc[outliers == 1].reset_index(drop=True)

    def outliers_sgd_one_class_svm(self):
        numeric_columns = self.column_types.numeric
        if self.check_nans(numeric_columns):
            self.miss_insert_mean_mode()
        outliers = SGDOneClassSVM().fit_predict(self.df[numeric_columns])
        self.df = self.df.loc[outliers == 1].reset_index(drop=True)

    # CANCELLED FOR FIRST ITERATION:
    # def outliers_three_sigma(self):
    # def outliers_grubbs(self):
    # def outliers_approximate(self):
    # def outliers_interquartile_distance(self):

    # CHAPTER 4: FEATURE SELECTION (required: all columns are numeric)---------

    def fs_select_percentile(self, param: int = 10):
        percentile = int(param)
        if self.check_categorical():
            self.error.append('categorical_select')
            return
        target = self.column_types.target
        x, y = self.df.drop(target, axis=1), self.df[target]
        if self.column_types.task_type.value == 'classification':
            selector = SelectPercentile(f_classif, percentile=percentile)
        else:
            selector = SelectPercentile(f_regression, percentile=percentile)
        selector.fit(x, y)
        selected_columns = self.df.columns[
            selector.get_support(indices=True)
        ].to_list()
        self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
        self.df[target] = y
        self.column_types.numeric = selected_columns
        self.update_pipeline = True

    def fs_select_k_best(self, param: int = 10):
        k = int(param)
        if self.check_categorical():
            self.error.append('categorical_select')
            return
        target = self.column_types.target
        x, y = self.df.drop(target, axis=1), self.df[target]
        if self.column_types.task_type.value == 'classification':
            selector = SelectKBest(f_classif, k=k)
        else:
            selector = SelectKBest(f_regression, k=k)
        selector.fit(x, y)
        selected_columns = self.df.columns[
            selector.get_support(indices=True)
        ].to_list()
        self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
        self.df[target] = y
        self.column_types.numeric = selected_columns
        self.update_pipeline = True

    def fs_select_fpr(self, param: float = 5e-2):
        alpha = param
        if self.check_categorical():
            self.error.append('categorical_select')
            return
        target = self.column_types.target
        x, y = self.df.drop(target, axis=1), self.df[target]
        if self.column_types.task_type.value == 'classification':
            selector = SelectFpr(f_classif, alpha=alpha)
        else:
            selector = SelectFpr(f_regression, alpha=alpha)
        selector.fit(x, y)
        selected_columns = self.df.columns[
            selector.get_support(indices=True)
        ].to_list()
        self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
        self.df[target] = y
        self.column_types.numeric = selected_columns
        self.update_pipeline = True

    def fs_select_fdr(self, param: float = 5e-2):
        alpha = param
        if self.check_categorical():
            self.error.append('categorical_select')
            return
        target = self.column_types.target
        x, y = self.df.drop(target, axis=1), self.df[target]
        if self.column_types.task_type.value == 'classification':
            selector = SelectFdr(f_classif, alpha=alpha)
        else:
            selector = SelectFdr(f_regression, alpha=alpha)
        selector.fit(x, y)
        selected_columns = self.df.columns[
            selector.get_support(indices=True)
        ].to_list()
        self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
        self.df[target] = y
        self.column_types.numeric = selected_columns
        self.update_pipeline = True

    def fs_select_fwe(self, param: float = 5e-2):
        alpha = param
        if self.check_categorical():
            self.error.append('categorical_select')
            return
        target = self.column_types.target
        x, y = self.df.drop(target, axis=1), self.df[target]
        if self.column_types.task_type.value == 'classification':
            selector = SelectFwe(f_classif, alpha=alpha)
        else:
            selector = SelectFwe(f_regression, alpha=alpha)
        selector.fit(x, y)
        selected_columns = self.df.columns[
            selector.get_support(indices=True)
        ].to_list()
        self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
        self.df[target] = y
        self.column_types.numeric = selected_columns
        self.update_pipeline = True

    def fs_select_rfe(self, param: int = None):
        n_features_to_select = int(param)
        if self.check_categorical():
            self.error.append('categorical_select')
            return
        target = self.column_types.target
        x, y = self.df.drop(target, axis=1), self.df[target]
        if self.column_types.task_type.value == 'classification':
            selector = RFE(
                LogisticRegression(), n_features_to_select=n_features_to_select
            )
        else:
            selector = RFE(
                LinearRegression(), n_features_to_select=n_features_to_select
            )
        selector.fit(x, y)
        selected_columns = self.df.columns[
            selector.get_support(indices=True)
        ].to_list()
        self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
        self.df[target] = y
        self.column_types.numeric = selected_columns
        self.update_pipeline = True

    def fs_select_from_model(self, param: int = None):
        max_features = int(param)
        if self.check_categorical():
            self.error.append('categorical_select')
            return
        target = self.column_types.target
        x, y = self.df.drop(target, axis=1), self.df[target]
        if self.column_types.task_type.value == 'classification':
            selector = SelectFromModel(
                LogisticRegression(), max_features=max_features
            )
        else:
            selector = SelectFromModel(
                LinearRegression(), max_features=max_features
            )
        selector.fit(x, y)
        selected_columns = self.df.columns[
            selector.get_support(indices=True)
        ].to_list()
        self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
        self.df[target] = y
        self.column_types.numeric = selected_columns
        self.update_pipeline = True

    def fs_select_pca(self, param: int = None):
        n_components = int(param)
        if self.check_categorical():
            self.error.append('categorical_select')
            return
        target = self.column_types.target
        x, y = self.df.drop(target, axis=1), self.df[target]
        if n_components is None:
            selector = PCA().fit(x)
            n_components = len(
                selector.singular_values_[selector.singular_values_ > 1]
            )
        selector = PCA(n_components=n_components)
        selector.fit(x)
        selected_columns = [f'PC{i}' for i in range(1, n_components + 1)]
        self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
        self.df[target] = y
        self.column_types.numeric = selected_columns
        self.update_pipeline = True
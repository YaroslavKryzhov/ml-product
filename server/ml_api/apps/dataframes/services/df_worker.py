from typing import List, Any, Callable, Dict

import pandas as pd
from sklearn import feature_selection, preprocessing, ensemble, covariance, \
    linear_model, svm, neighbors

import ml_api.apps.dataframes.schemas as schemas
import ml_api.apps.dataframes.specs as specs


class ApplyFunctionException(Exception):
    pass


class DataframeFunctionProcessor:
    def __init__(self, dataframe: pd.DataFrame,
                 column_types: schemas.ColumnTypes):
        self._df: pd.DataFrame = dataframe
        self._column_types: schemas.ColumnTypes = column_types
        self._pipeline: List[schemas.PipelineElement] = []
        self._functions_map: Dict[specs.AvailableFunctions, Callable] = {
            specs.AvailableFunctions.remove_duplicates: self._remove_duplicates,
            specs.AvailableFunctions.drop_na: self._drop_na,
            specs.AvailableFunctions.drop_column: self._drop_column,
            specs.AvailableFunctions.miss_insert_mean_mode: self._miss_insert_mean_mode,
            specs.AvailableFunctions.miss_linear_imputer: self._miss_linear_imputer,
            specs.AvailableFunctions.miss_knn_imputer: self._miss_knn_imputer,
            specs.AvailableFunctions.standardize_features: self._standardize_features,
            specs.AvailableFunctions.ordinal_encoding: self._ordinal_encoding,
            specs.AvailableFunctions.one_hot_encoding: self._one_hot_encoding,
            specs.AvailableFunctions.outliers_isolation_forest: self._outliers_isolation_forest,
            specs.AvailableFunctions.outliers_elliptic_envelope: self._outliers_elliptic_envelope,
            specs.AvailableFunctions.outliers_local_factor: self._outliers_local_factor,
            specs.AvailableFunctions.outliers_one_class_svm: self._outliers_one_class_svm,
            specs.AvailableFunctions.outliers_sgd_one_class_svm: self._outliers_sgd_one_class_svm,
            # specs.AvailableFunctions.fs_select_percentile: self.fs_select_percentile,
            # specs.AvailableFunctions.fs_select_k_best: self.fs_select_k_best,
            # specs.AvailableFunctions.fs_select_fpr: self.fs_select_fpr,
            # specs.AvailableFunctions.fs_select_fdr: self.fs_select_fdr,
            # specs.AvailableFunctions.fs_select_fwe: self.fs_select_fwe,
            # specs.AvailableFunctions.fs_select_rfe: self.fs_select_rfe,
            # specs.AvailableFunctions.fs_select_from_model: self.fs_select_from_model,
            # specs.AvailableFunctions.fs_select_pca: self.fs_select_pca,
        }

    def get_df(self) -> pd.DataFrame:
        return self._df

    def get_column_types(self) -> schemas.ColumnTypes:
        return self._column_types

    def get_pipeline(self) -> List[schemas.PipelineElement]:
        return self._pipeline

    def _update_pipeline(self, function_name: specs.AvailableFunctions,
                         params: Any = None):
        self._pipeline.append(schemas.PipelineElement(
            function_name=function_name, params=params))

    def is_pipelined_once(self) -> bool:
        size = len(self._pipeline)
        if size == 1:
            return True
        elif size > 1:
            raise ApplyFunctionException(
                'Many elements in pipeline (0/1 was expected)')
        else:
            return False

    def apply_function(self, function_name: specs.AvailableFunctions,
                       params: Any = None):
        func = self._functions_map.get(function_name, self._no_func_error)
        func(params)

    def _no_func_error(self):
        raise ApplyFunctionException(
            'Unavailable function: Function not found in DocumentOperator.functions_map')

    def _have_nans(self, columns) -> bool:
        return self._df[columns].isna().sum().sum() > 0

    def _have_categorical(self) -> bool:
        return len(self._column_types.categorical) > 0

    def _remove_target_from_columns(self, columns_list):
        try:
            columns_list.remove(self._column_types.target)
        except ValueError:
            pass

    # CHAPTER 1: MISSING DATA AND DUPLICATES-----------------------------------

    def _remove_duplicates(self, params):
        self.update_pipeline = True
        self._df.drop_duplicates(inplace=True)

    def _drop_na(self, params):
        self.update_pipeline = True
        self._df.dropna(inplace=True)

    def _drop_column(self, params: str):
        column = params
        try:
            self._df.drop(column, axis=1, inplace=True)
        except KeyError:
            raise ApplyFunctionException(
                f"Column {column} not found in dataframe.")
        if self._column_types.target == column:
            self._column_types.target = None
        try:
            self._column_types.numeric.remove(column)
        except ValueError:
            try:
                self._column_types.categorical.remove(column)
            except ValueError:
                raise ApplyFunctionException(
                    f"DANGER! (drop_column): Name not in categorical or numeric column_types")
        self._update_pipeline(specs.AvailableFunctions.drop_column, params)

    def _miss_insert_mean_mode(self, params):
        numeric_columns = self._column_types.numeric
        categorical_columns = self._column_types.categorical
        self._df[numeric_columns] = pd.DataFrame(
            feature_selection.SimpleImputer(strategy='mean').fit_transform(
                self._df[numeric_columns]
            ),
            self._df.index,
            numeric_columns,
        )
        self._df[categorical_columns] = pd.DataFrame(
            feature_selection.SimpleImputer(
                strategy='most_frequent').fit_transform(
                self._df[categorical_columns]
            ),
            self._df.index,
            categorical_columns,
        )

    def _miss_linear_imputer(self, params):
        numeric_columns = self._column_types.numeric
        self._df[numeric_columns] = pd.DataFrame(
            feature_selection.IterativeImputer(
            ).fit_transform(self._df[numeric_columns]),
            self._df.index,
            numeric_columns,
        )

    def _miss_knn_imputer(self, params):
        numeric_columns = self._column_types.numeric
        self._df[numeric_columns] = pd.DataFrame(
            feature_selection.KNNImputer(
            ).fit_transform(self._df[numeric_columns]),
            self._df.index,
            numeric_columns,
        )

    # CHAPTER 2: FEATURE TRANSFORMATION (required: no NaN values)--------------
    def _standardize_features(self, params):
        numeric_columns = self._column_types.numeric
        self._remove_target_from_columns(numeric_columns)
        if self._have_nans(numeric_columns):
            self._miss_insert_mean_mode()  # не работает на пропусках в данных
        sc = preprocessing.StandardScaler()
        self._df[numeric_columns] = pd.DataFrame(
            sc.fit_transform(self._df[numeric_columns]),
            self._df.index,
            numeric_columns,
        )
        self._update_pipeline(specs.AvailableFunctions.standardize_features)

    def _ordinal_encoding(self, params):
        categorical = self._column_types.categorical
        self._remove_target_from_columns(categorical)
        if self._have_nans(categorical):
            self._miss_insert_mean_mode()  # не работает на пропусках в данных
        self._df[categorical] = preprocessing.OrdinalEncoder().fit_transform(
            self._df[categorical]
        )
        self._column_types.numeric.extend(categorical)
        self._column_types.categorical = []
        self._update_pipeline(specs.AvailableFunctions.ordinal_encoding)

    def _one_hot_encoding(self, params):
        categorical = self._column_types.categorical
        self._remove_target_from_columns(categorical)
        if self._have_nans(categorical):
            self._miss_insert_mean_mode()  # не работает на пропусках в данных
        enc = preprocessing.OneHotEncoder()
        enc.fit(self._df[categorical])
        new_cols = enc.get_feature_names_out(categorical)
        self._df[new_cols] = enc.transform(self._df[categorical]).toarray()
        self._df.drop(categorical, axis=1, inplace=True)
        self._column_types.numeric.extend(new_cols)
        self._column_types.categorical = []
        self._update_pipeline(specs.AvailableFunctions.one_hot_encoding)

    # CHAPTER 3: OUTLIERS (required: no NaN values)----------------------------
    def _outliers_isolation_forest(self, params):
        numeric_columns = self._column_types.numeric
        self._remove_target_from_columns(numeric_columns)
        if self._have_nans(numeric_columns):
            self._miss_insert_mean_mode()  # не работает на пропусках в данных
        outliers = ensemble.IsolationForest().fit_predict(
            self._df[numeric_columns])
        self._df = self._df.loc[outliers == 1].reset_index(drop=True)

    def _outliers_elliptic_envelope(self, params):
        numeric_columns = self._column_types.numeric
        self._remove_target_from_columns(numeric_columns)
        if self._have_nans(numeric_columns):
            self._miss_insert_mean_mode()  # не работает на пропусках в данных
        outliers = covariance.EllipticEnvelope().fit_predict(
            self._df[numeric_columns])
        self._df = self._df.loc[outliers == 1].reset_index(drop=True)

    def _outliers_local_factor(self, params):
        numeric_columns = self._column_types.numeric
        self._remove_target_from_columns(numeric_columns)
        if self._have_nans(numeric_columns):
            self._miss_insert_mean_mode()  # не работает на пропусках в данных
        outliers = neighbors.LocalOutlierFactor().fit_predict(
            self._df[numeric_columns])
        self._df = self._df.loc[outliers == 1].reset_index(drop=True)

    def _outliers_one_class_svm(self, params):
        numeric_columns = self._column_types.numeric
        self._remove_target_from_columns(numeric_columns)
        if self._have_nans(numeric_columns):
            self._miss_insert_mean_mode()  # не работает на пропусках в данных
        outliers = svm.OneClassSVM().fit_predict(self._df[numeric_columns])
        self._df = self._df.loc[outliers == 1].reset_index(drop=True)

    def _outliers_sgd_one_class_svm(self, params):
        numeric_columns = self._column_types.numeric
        self._remove_target_from_columns(numeric_columns)
        if self._have_nans(numeric_columns):
            self._miss_insert_mean_mode()  # не работает на пропусках в данных
        outliers = linear_model.SGDOneClassSVM().fit_predict(
            self._df[numeric_columns])
        self._df = self._df.loc[outliers == 1].reset_index(drop=True)

    # CANCELLED FOR FIRST(SECOND) ITERATION:
    # def outliers_three_sigma(self):
    # def outliers_grubbs(self):
    # def outliers_approximate(self):
    # def outliers_interquartile_distance(self):

    # CHAPTER 4: FEATURE SELECTION (required: all columns are numeric)---------
    # CANCELLED FOR SECOND ITERATION
    # TO DO: refactor FeatureSelection()
    """
        Позже: проверить логику, протестировать и обдумать, как применять 
        преобразования к тестовой выборке.
        Скорее всего понадобится сохранять преобразование. 
        Пока это выглядит запарно.
        
        Нельзя запускать методы без целевого признака.
        Нельзя запускать методы на категориальных признаках.
        Еще нужно знать тип задачи - regr/class
        Учитываем, что целевой признак 
        тоже в списках column_types.numeric/categorical.
    """
    # def fs_select_percentile(self, param: int = 10):
    #     percentile = int(param)
    #     if self.check_categorical():
    #         self.error.append('categorical_select')
    #         return
    #     target = self.column_types.target
    #     x, y = self.df.drop(target, axis=1), self.df[target]
    #     if self.column_types.task_type.value == 'classification':
    #         selector = feature_selection.SelectPercentile(feature_selection.f_classif, percentile=percentile)
    #     else:
    #         selector = feature_selection.SelectPercentile(feature_selection.f_regression, percentile=percentile)
    #     selector.fit(x, y)
    #     selected_columns = self.df.columns[
    #         selector.get_support(indices=True)
    #     ].to_list()
    #     self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
    #     self.df[target] = y
    #     self.column_types.numeric = selected_columns
    #     self.update_pipeline = True
    #
    # def fs_select_k_best(self, param: int = 10):
    #     k = int(param)
    #     if self.check_categorical():
    #         self.error.append('categorical_select')
    #         return
    #     target = self.column_types.target
    #     x, y = self.df.drop(target, axis=1), self.df[target]
    #     if self.column_types.task_type.value == 'classification':
    #         selector = feature_selection.SelectKBest(feature_selection.f_classif, k=k)
    #     else:
    #         selector = feature_selection.SelectKBest(feature_selection.f_regression, k=k)
    #     selector.fit(x, y)
    #     selected_columns = self.df.columns[
    #         selector.get_support(indices=True)
    #     ].to_list()
    #     self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
    #     self.df[target] = y
    #     self.column_types.numeric = selected_columns
    #     self.update_pipeline = True
    #
    # def fs_select_fpr(self, param: float = 5e-2):
    #     alpha = param
    #     if self.check_categorical():
    #         self.error.append('categorical_select')
    #         return
    #     target = self.column_types.target
    #     x, y = self.df.drop(target, axis=1), self.df[target]
    #     if self.column_types.task_type.value == 'classification':
    #         selector = feature_selection.SelectFpr(feature_selection.f_classif, alpha=alpha)
    #     else:
    #         selector = feature_selection.SelectFpr(feature_selection.f_regression, alpha=alpha)
    #     selector.fit(x, y)
    #     selected_columns = self.df.columns[
    #         selector.get_support(indices=True)
    #     ].to_list()
    #     self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
    #     self.df[target] = y
    #     self.column_types.numeric = selected_columns
    #     self.update_pipeline = True
    #
    # def fs_select_fdr(self, param: float = 5e-2):
    #     alpha = param
    #     if self.check_categorical():
    #         self.error.append('categorical_select')
    #         return
    #     target = self.column_types.target
    #     x, y = self.df.drop(target, axis=1), self.df[target]
    #     if self.column_types.task_type.value == 'classification':
    #         selector = feature_selection.SelectFdr(feature_selection.f_classif, alpha=alpha)
    #     else:
    #         selector = feature_selection.SelectFdr(feature_selection.f_regression, alpha=alpha)
    #     selector.fit(x, y)
    #     selected_columns = self.df.columns[
    #         selector.get_support(indices=True)
    #     ].to_list()
    #     self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
    #     self.df[target] = y
    #     self.column_types.numeric = selected_columns
    #     self.update_pipeline = True
    #
    # def fs_select_fwe(self, param: float = 5e-2):
    #     alpha = param
    #     if self.check_categorical():
    #         self.error.append('categorical_select')
    #         return
    #     target = self.column_types.target
    #     x, y = self.df.drop(target, axis=1), self.df[target]
    #     if self.column_types.task_type.value == 'classification':
    #         selector = feature_selection.SelectFwe(feature_selection.f_classif, alpha=alpha)
    #     else:
    #         selector = feature_selection.SelectFwe(feature_selection.f_regression, alpha=alpha)
    #     selector.fit(x, y)
    #     selected_columns = self.df.columns[
    #         selector.get_support(indices=True)
    #     ].to_list()
    #     self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
    #     self.df[target] = y
    #     self.column_types.numeric = selected_columns
    #     self.update_pipeline = True
    #
    # def fs_select_rfe(self, param: int = None):
    #     n_features_to_select = int(param)
    #     if self.check_categorical():
    #         self.error.append('categorical_select')
    #         return
    #     target = self.column_types.target
    #     x, y = self.df.drop(target, axis=1), self.df[target]
    #     if self.column_types.task_type.value == 'classification':
    #         selector = feature_selection.RFE(
    #             linear_model.LogisticRegression(), n_features_to_select=n_features_to_select
    #         )
    #     else:
    #         selector = feature_selection.RFE(
    #             linear_model.LinearRegression(), n_features_to_select=n_features_to_select
    #         )
    #     selector.fit(x, y)
    #     selected_columns = self.df.columns[
    #         selector.get_support(indices=True)
    #     ].to_list()
    #     self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
    #     self.df[target] = y
    #     self.column_types.numeric = selected_columns
    #     self.update_pipeline = True
    #
    # def fs_select_from_model(self, param: int = None):
    #     max_features = int(param)
    #     if self.check_categorical():
    #         self.error.append('categorical_select')
    #         return
    #     target = self.column_types.target
    #     x, y = self.df.drop(target, axis=1), self.df[target]
    #     if self.column_types.task_type.value == 'classification':
    #         selector = feature_selection.SelectFromModel(
    #             linear_model.LogisticRegression(), max_features=max_features
    #         )
    #     else:
    #         selector = feature_selection.SelectFromModel(
    #             linear_model.LinearRegression(), max_features=max_features
    #         )
    #     selector.fit(x, y)
    #     selected_columns = self.df.columns[
    #         selector.get_support(indices=True)
    #     ].to_list()
    #     self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
    #     self.df[target] = y
    #     self.column_types.numeric = selected_columns
    #     self.update_pipeline = True
    #
    # def fs_select_pca(self, param: int = None):
    #     n_components = int(param)
    #     if self.check_categorical():
    #         self.error.append('categorical_select')
    #         return
    #     target = self.column_types.target
    #     x, y = self.df.drop(target, axis=1), self.df[target]
    #     if n_components is None:
    #         selector = decomposition.PCA().fit(x)
    #         n_components = len(
    #             selector.singular_values_[selector.singular_values_ > 1]
    #         )
    #     selector = decomposition.PCA(n_components=n_components)
    #     selector.fit(x)
    #     selected_columns = [f'PC{i}' for i in range(1, n_components + 1)]
    #     self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
    #     self.df[target] = y
    #     self.column_types.numeric = selected_columns
    #     self.update_pipeline = True

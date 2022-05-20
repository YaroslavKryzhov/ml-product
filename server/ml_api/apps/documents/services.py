from calendar import c
from nis import cat
from unicodedata import numeric
import pandas as pd
import numpy as np
from datetime import datetime
from outliers import smirnov_grubbs as grubbs
from typing import List, Union, Dict, Callable, Tuple, Optional
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import IsolationForest
from scipy.stats import mode
from sklearn.svm import OneClassSVM, SVR
from sklearn.preprocessing import OrdinalEncoder, StandardScaler, OneHotEncoder
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
from sklearn.feature_selection import SelectKBest, f_classif, SelectFpr, SelectFwe, SelectFdr, RFE, SelectFromModel, \
    SelectPercentile, VarianceThreshold, GenericUnivariateSelect
from sklearn.decomposition import PCA
from sklearn.base import BaseEstimator

from sympy import numer, per

from ml_api.apps.documents.repository import DocumentFileCRUD, DocumentPostgreCRUD


class DocumentService:

    def __init__(self, db, user):
        self._db = db
        self._user = user

    def upload_document_to_db(self, file, filename: str):
        document = DocumentPostgreCRUD(self._db, self._user).read_document_by_name(filename)
        if document is not None:
            return document['name']
        DocumentFileCRUD(self._user).upload_document(filename, file)
        DocumentPostgreCRUD(self._db, self._user).new_document(filename)
        return True

    def read_document_from_db(self, filename: str, page: int = 1, rows_on_page: int = 50) -> pd.DataFrame:
        if DocumentPostgreCRUD(self._db, self._user).read_document_by_name(filename=filename) is not None:
            df = DocumentFileCRUD(self._user).read_document(filename)
            start_index = (page - 1) * rows_on_page
            stop_index = page * rows_on_page
            try:
                result = df.iloc[start_index:stop_index]
            except IndexError:
                try:
                    result = df.iloc[start_index:]
                except IndexError:
                    return pd.DataFrame()
                else:
                    return result
            else:
                return result
        return None

    def get_document_stat_info(self, filename: str) -> pd.DataFrame:
        if DocumentPostgreCRUD(self._db, self._user).read_document_by_name(filename=filename) is not None:
            df = DocumentFileCRUD(self._user).read_document(filename)
            import io
            buffer = io.StringIO()
            df.info(buf=buffer)
            lines = buffer.getvalue().splitlines()
            df = (pd.DataFrame([x.split() for x in lines[5:-2]], columns=lines[3].split())
                  .drop(['#','Count'], axis=1))
            return df
        return None

    def get_document_stat_description(self, filename: str) -> pd.DataFrame:
        if DocumentPostgreCRUD(self._db, self._user).read_document_by_name(filename=filename) is not None:
            df = DocumentFileCRUD(self._user).read_document(filename)
            return df.describe()
        return None

    def get_column_stat_description(self, filename: str, column_name: str) -> [str, str]:
        if DocumentPostgreCRUD(self._db, self._user).read_document_by_name(filename=filename) is not None:
            df = DocumentFileCRUD(self._user).read_document(filename)
            column_marks = self.read_column_marks(filename)
            if column_name in column_marks['numeric']:
                return ['numeric', pd.cut(df[column_name], 10).value_counts().sort_index().to_json()]
            elif column_name in column_marks['categorical']:
                return ['categorical', df[column_name].value_counts().to_json()]
            elif column_name in column_marks['target']:
                try:
                    result = ['target', pd.cut(df[column_name], 10).value_counts().sort_index().to_json()]
                except TypeError:
                    result = ['target', df[column_name].value_counts().to_json()]
                return result
        return None

    def read_document_info(self, filename: str):
        document = DocumentPostgreCRUD(self._db, self._user).read_document_by_name(filename=filename)
        return document

    def read_documents_info(self):
        documents = DocumentPostgreCRUD(self._db, self._user).read_all_documents_by_user()
        return documents

    def download_document_from_db(self, filename: str):
        file = DocumentFileCRUD(self._user).download_document(filename)
        return file

    def rename_document(self, filename: str, new_filename: str):
        DocumentFileCRUD(self._user).rename_document(filename, new_filename)
        query = {
            'name': new_filename
        }
        DocumentPostgreCRUD(self._db, self._user).update_document(filename, query)

    def update_change_date_in_db(self, filename: str):
        query = {
            'change_date': str(datetime.now())
        }
        DocumentPostgreCRUD(self._db, self._user).update_document(filename, query)

    def delete_document_from_db(self, filename: str):
        DocumentFileCRUD(self._user).delete_document(filename)
        DocumentPostgreCRUD(self._db, self._user).delete_document(filename)

    def read_pipeline(self, filename: str):
        pipeline = DocumentPostgreCRUD(self._db, self._user).read_document_by_name(filename)['pipeline']
        return pipeline

    def update_pipeline(self, filename: str, method: str):
        pipeline = self.read_pipeline(filename)
        pipeline.append(method)
        query = {
            'pipeline': pipeline
        }
        DocumentPostgreCRUD(self._db, self._user).update_document(filename, query)

    def read_documents_columns(self, filename: str):
        df = DocumentFileCRUD(self._user).read_document(filename)
        return df.columns.to_list()

    def read_column_marks(self, filename: str) -> Dict:
        column_marks = dict(DocumentPostgreCRUD(self._db, self._user).read_document_by_name(filename)['column_marks'])
        return column_marks

    def update_column_marks(self, filename: str, column_marks: Dict[str, Union[List[str], str]]):
        query = {
            'column_marks': column_marks
        }
        DocumentPostgreCRUD(self._db, self._user).update_document(filename, query)

    def apply_pipeline_to_csv(self, filename: str, pipeline: List[str]):
        for function_name in pipeline:
            self.apply_function(filename=filename, function_name=function_name)

    def apply_function(self, filename: str, function_name: str):
        document = DocumentFileCRUD(self._user).read_document(filename)
        column_marks = self.read_column_marks(filename)
        document_operator = DocumentOperator(document, column_marks)

        if function_name == 'remove_duplicates':
            document_operator.remove_duplicates()
        elif function_name == 'drop_na':
            document_operator.drop_na()
        elif function_name == 'miss_insert_mean_mode':
            document_operator.miss_insert_mean_mode()
        elif function_name == 'miss_linear_imputer':
            document_operator.miss_linear_imputer()

        elif function_name == 'standardize_features':
            document_operator.standardize_features()
            self.update_pipeline(filename, method='standardize_features')
        elif function_name == 'ordinal_encoding':
            document_operator.ordinal_encoding()
            self.update_pipeline(filename, method='ordinal_encoding')
            self.update_column_marks(filename, column_marks=document_operator.get_column_marks())
        elif function_name == 'one_hot_encoding':
            document_operator.one_hot_encoding()
            self.update_pipeline(filename, method='one_hot_encoding')
            self.update_column_marks(filename, column_marks=document_operator.get_column_marks())

        elif function_name == 'outliers_isolation_forest':
            document_operator.outliers_isolation_forest()
        elif function_name == 'outliers_elliptic_envelope':
            document_operator.outliers_elliptic_envelope()
        elif function_name == 'outliers_local_factor':
            document_operator.outliers_local_factor()
        elif function_name == 'outliers_one_class_svm':
            document_operator.outliers_one_class_svm()
        # elif function_name == 'outliers_three_sigma':
        #     document_operator.outliers_three_sigma()

        elif function_name == 'fs_select_k_best':
            document_operator.fs_select_k_best()
            self.update_pipeline(filename, method='fs_select_k_best')
            self.update_column_marks(filename, column_marks=document_operator.get_column_marks())
        elif function_name == 'fs_select_fpr':
            document_operator.fs_select_fpr()
            self.update_pipeline(filename, method='fs_select_fpr')
            self.update_column_marks(filename, column_marks=document_operator.get_column_marks())

        DocumentFileCRUD(self._user).update_document(filename, document_operator.get_df())
        self.update_change_date_in_db(filename)


class DocumentOperator:

    def __init__(self, document: pd.DataFrame, column_marks: Dict[str, Union[List[str], str]]):
        self.df = document
        self.column_marks = column_marks

    def get_df(self) -> pd.DataFrame:
        return self.df

    def get_column_marks(self) -> Dict[str, Union[List[str], str]]:
        return self.column_marks

    # CHAPTER 1: MISSING DATA AND DUPLICATES----------------------------------------------------------------------------

    def remove_duplicates(self):
        self.df.drop_duplicates(inplace=True)

    def drop_na(self):
        self.df.dropna(inplace=True)

    def miss_insert_mean_mode(self):
        numeric_columns = self.column_marks['numeric']
        categorical = self.column_marks['categorical']
        for feature in self.df.columns:
            if feature in categorical:
                self.df[feature].fillna(mode(self.df[feature]).mode[0], inplace=True)
            if feature in numeric_columns:
                self.df[feature].fillna(self.df[feature].mean(), inplace=True)

    def miss_linear_imputer(self):  # can be slow on big amount of columns
        numeric_columns = self.column_marks['numeric']
        self.df[numeric_columns] = pd.DataFrame(IterativeImputer().fit_transform(self.df[numeric_columns]))

    # CHAPTER 2: FEATURE TRANSFORMATION---------------------------------------------------------------------------------

    def standardize_features(self):
        numeric_columns = self.column_marks['numeric']
        sc = StandardScaler()
        self.df[numeric_columns] = pd.DataFrame(sc.fit_transform(self.df[numeric_columns]), self.df.index,
                                                numeric_columns)

    def ordinal_encoding(self):
        categorical = self.column_marks['categorical']
        self.df[categorical] = OrdinalEncoder().fit_transform(self.df[categorical])

        self.column_marks['numeric'].extend(categorical)
        self.column_marks['categorical'] = []

    def one_hot_encoding(self):
        categorical = self.column_marks['categorical']
        enc = OneHotEncoder()
        enc.fit(self.df[categorical])
        new_cols = enc.get_feature_names(categorical)
        self.df[new_cols] = enc.transform(self.df[categorical]).toarray()
        self.df.drop(categorical, axis=1, inplace=True)

        self.column_marks['numeric'].extend(new_cols)
        self.column_marks['categorical'] = []

    # CHAPTER 3: OUTLIERS-----------------------------------------------------------------------------------------------

    def outliers_isolation_forest(self):
        numeric_columns = self.column_marks['numeric']
        outliers = IsolationForest().fit_predict(self.df[numeric_columns])
        self.df = self.df.loc[outliers == 1].reset_index(drop=True)

    def outliers_elliptic_envelope(self):
        numeric_columns = self.column_marks['numeric']
        outliers = EllipticEnvelope().fit_predict(self.df[numeric_columns])
        self.df = self.df.loc[outliers == 1].reset_index(drop=True)

    def outliers_local_factor(self):
        numeric_columns = self.column_marks['numeric']
        outliers = LocalOutlierFactor().fit_predict(self.df[numeric_columns])
        self.df = self.df.loc[outliers == 1].reset_index(drop=True)

    def outliers_one_class_svm(self):
        numeric_columns = self.column_marks['numeric']
        outliers = OneClassSVM().fit_predict(self.df[numeric_columns])
        self.df = self.df.loc[outliers == 1].reset_index(drop=True)

    # def outliers_three_sigma(self):
    #     numeric_columns = self.column_marks['numeric']
    #     self.df[numeric_columns] = self.df.loc[(self.df[numeric_columns] -
    #             self.df[numeric_columns].mean()).abs() < 3 * self.df.std(), numeric_columns].dropna(axis=0, how='any')

    # def outliers_grubbs(self):
    #     alpha = 0.05
    #     numeric_columns = self.column_marks['numeric']
    #     for col in numeric_columns:
    #         self.df = self.df.drop(
    #             grubbs.two_sided_test_indices(self.df[col], alpha)
    #         ).reset_index().drop('index', axis=1)
    #
    # def outliers_approximate(self):
    #     deviation =
    #     numeric_columns = self.column_marks['numeric']
    #     M = self.df[numeric_columns]
    #     u, s, vh = np.linalg.svd(M, full_matrices=True)
    #     Mk_rank = np.linalg.matrix_rank(M) - deviation
    #     Uk, Sk, VHk = u[:, :Mk_rank], np.diag(s)[:Mk_rank, :Mk_rank], vh[:Mk_rank, :]
    #     Mk = pd.DataFrame(np.dot(np.dot(Uk, Sk), VHk), index=M.index, columns=M.columns)
    #     delta = abs(Mk - M)
    #     self.df = self.df.drop(delta.idxmax())
    #
    # def outliers_interquartile_distance(self, low_quantile: float, up_quantile: float, coef: float):
    #     numeric_columns = self.column_marks['numeric']
    #     self.df
    #     quantile = numeric_columns.quantile([low_quantile, up_quantile])
    #     for column in numeric_columns:
    #         low_lim = quantile[column][low_quantile]
    #         up_lim = quantile[column][up_quantile]
    #         df = df.loc[df[column] >= low_lim - coef * (up_lim - low_lim)]. \
    #             loc[df[column] <= up_lim + coef * (up_lim - low_lim)]

    # CHAPTER 4: FEATURE SELECTION--------------------------------------------------------------------------------------

    def fs_select_k_best(self, k: int = 10):
        target = self.column_marks['target']
        X, y = self.df.drop(target, axis=1), self.df[target]
        # TOD: add changing score function
        # TOD: add k parameter selection
        selector = SelectKBest(k=k)
        selector.fit(X, y)
        self.df = pd.DataFrame(selector.transform(X), columns=self.df.columns[selector.get_support(indices=True)])
        self.df[target] = y
        # TOD: add column_marks changer

    # def fs_select_fpr(
    #         self,
    #         filename: str,
    #         score_func: Callable[
    #             [np.ndarray, np.ndarray],
    #             Tuple[np.ndarray, np.ndarray]
    #         ] = f_classif,
    #         alpha: Union[int, str] = 0.05
    # ):
    #     document = DocumentFileCRUD(self._user).read_document(filename)
    #     columns_dict = self.read_column_marks(filename)
    #     x = columns_dict['numeric'].append(columns_dict['categorical'])
    #     y = columns_dict['target']
    #     selector = SelectFpr(score_func=score_func, alpha=alpha)
    #     selector.fit(x, y)
    #     document = pd.DataFrame(selector.transform(x), columns=document.columns[selector.get_support(indices=True)])
    #     document['target'] = y
    #     self.update_change_date_in_db(filename)
    #     DocumentFileCRUD(self._user).update_document(filename, document)
    #     self.update_pipeline(filename, method='fs_select_fpr')
    #
    # def fs_select_fwe(
    #         self,
    #         filename: str,
    #         score_func: Callable[
    #             [np.ndarray, np.ndarray],
    #             Tuple[np.ndarray, np.ndarray]
    #         ] = f_classif,
    #         alpha: Union[int, str] = 0.05
    # ):
    #     document = DocumentFileCRUD(self._user).read_document(filename)
    #     columns_dict = self.read_column_marks(filename)
    #     x = columns_dict['numeric'].append(columns_dict['categorical'])
    #     y = columns_dict['target']
    #     selector = SelectFwe(score_func=score_func, alpha=alpha)
    #     selector.fit(x, y)
    #     document = pd.DataFrame(selector.transform(x), columns=document.columns[selector.get_support(indices=True)])
    #     document['target'] = y
    #     self.update_change_date_in_db(filename)
    #     DocumentFileCRUD(self._user).update_document(filename, document)
    #     self.update_pipeline(filename, method='fs_select_fwe')
    #
    # def fs_select_fdr(
    #         self,
    #         filename: str,
    #         score_func: Callable[
    #             [np.ndarray, np.ndarray],
    #             Tuple[np.ndarray, np.ndarray]
    #         ] = f_classif,
    #         alpha: Union[int, str] = 0.05
    # ):
    #     document = DocumentFileCRUD(self._user).read_document(filename)
    #     columns_dict = self.read_column_marks(filename)
    #     x = columns_dict['numeric'].append(columns_dict['categorical'])
    #     y = columns_dict['target']
    #     selector = SelectFdr(score_func=score_func, alpha=alpha)
    #     selector.fit(x, y)
    #     document = pd.DataFrame(selector.transform(x), columns=document.columns[selector.get_support(indices=True)])
    #     document['target'] = y
    #     self.update_change_date_in_db(filename)
    #     DocumentFileCRUD(self._user).update_document(filename, document)
    #     self.update_pipeline(filename, method='fs_select_fdr')
    #
    # def fs_pca(self, filename: str, n_components: Optional[int]):
    #     document = DocumentFileCRUD(self._user).read_document(filename)
    #     target = self.read_column_marks(filename)['target']
    #     X, y = document.drop(target, axis=1), document[target]
    #     if n_components is None:
    #         pca = PCA().fit(X)
    #         n_components = len(pca.singular_values_[pca.singular_values_ > 1])
    #     document = pd.DataFrame(
    #         PCA(n_components=n_components).fit_transform(X),
    #         columns=[f'PC{i}' for i in range(1, n_components + 1)]
    #     )
    #     document[target] = y
    #     self.update_change_date_in_db(filename)
    #     DocumentFileCRUD(self._user).update_document(filename, document)
    #
    #     self.update_pipeline(filename, method='fs_pca')
    #
    # def fs_rfe(
    #         self,
    #         filename: str,
    #         estimator: BaseEstimator = SVR(kernel='linear'),
    #         n_features: Optional[int] = None,
    # ):
    #     document = DocumentFileCRUD(self._user).read_document(filename)
    #     target = self.read_column_marks(filename)['target']
    #     X, y = document.drop(target, axis=1), document[target]
    #     selector = RFE(estimator=estimator, n_features_to_select=n_features)
    #     selector.fit(X, y)
    #     document = pd.DataFrame(selector.transform(X), columns=X.columns[selector.support_])
    #     document[target] = y
    #     self.update_change_date_in_db(filename)
    #     DocumentFileCRUD(self._user).update_document(filename, document)
    #     self.update_pipeline(filename, method='fs_rfe')
    #
    # def fs_select_from_model(
    #         self,
    #         filename: str,
    #         estimator: BaseEstimator,
    #         threshold: Optional[Union[str, float]] = None,
    #         max_features: Optional[int] = None,
    # ):
    #     document = DocumentFileCRUD(self._user).read_document(filename)
    #     target = self.read_column_marks(filename)['target']
    #     X, y = document.drop(target, axis=1), document[target]
    #     selector = SelectFromModel(estimator=estimator, threshold=threshold, max_features=max_features)
    #     selector.fit(X, y)
    #     document = pd.DataFrame(selector.transform(X), columns=X.columns[selector.get_support()])
    #     document[target] = y
    #     self.update_change_date_in_db(filename)
    #     DocumentFileCRUD(self._user).update_document(filename, document)
    #     self.update_pipeline(filename, method='fs_select_from_model')
    #
    # def fs_select_percentile(
    #         self,
    #         filename: str,
    #         score_func: Callable[
    #             [np.ndarray, np.ndarray],
    #             Tuple[np.ndarray, np.ndarray]
    #         ] = f_classif,
    #         percentile: int = 10
    # ):
    #     document = DocumentFileCRUD(self._user).read_document(filename)
    #     X, y = document.drop('target', axis=1), document['target']
    #     selector = SelectPercentile(score_func=score_func, percentile=percentile)
    #     selector.fit(X, y)
    #     document = pd.DataFrame(selector.transform(X), columns=document.columns[selector.get_support(indices=True)])
    #     document['target'] = y
    #     self.update_change_date_in_db(filename)
    #     DocumentFileCRUD(self._user).update_document(filename, document)
    #     self.update_pipeline(filename, method='fs_select_percentile')
    #
    # def fs_variance_threshold(
    #         self,
    #         filename: str,
    #         threshold: float = 0.0
    # ):
    #     document = DocumentFileCRUD(self._user).read_document(filename)
    #     X, y = document.drop('target', axis=1), document['target']
    #     selector = VarianceThreshold(threshold=threshold)
    #     selector.fit(X, y)
    #     document = pd.DataFrame(selector.transform(X), columns=document.columns[selector.get_support(indices=True)])
    #     document['target'] = y
    #     self.update_change_date_in_db(filename)
    #     DocumentFileCRUD(self._user).update_document(filename, document)
    #     self.update_pipeline(filename, method='fs_variance_threshold')
    #
    # def fs_generic_univariate_select(
    #         self,
    #         filename: str,
    #         score_func: Callable[
    #             [np.ndarray, np.ndarray],
    #             Tuple[np.ndarray, np.ndarray]
    #         ] = f_classif,
    #         mode: str = 'percentile',
    #         param: Union[int, float] = 1e-5
    # ):
    #     document = DocumentFileCRUD(self._user).read_document(filename)
    #     X, y = document.drop('target', axis=1), document['target']
    #     selector = GenericUnivariateSelect(score_func=score_func, mode=mode, param=param)
    #     selector.fit(X, y)
    #     document = pd.DataFrame(selector.transform(X), columns=document.columns[selector.get_support(indices=True)])
    #     document['target'] = y
    #     self.update_change_date_in_db(filename)
    #     DocumentFileCRUD(self._user).update_document(filename, document)
    #     self.update_pipeline(filename, method='fs_generic_univariate_select')

from datetime import datetime
from typing import List, Union, Dict

import pandas as pd
from sklearn.experimental import enable_iterative_imputer # noqa
from sklearn.impute import IterativeImputer, SimpleImputer, KNNImputer
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.linear_model import SGDOneClassSVM, LogisticRegression, LinearRegression
from sklearn.preprocessing import OrdinalEncoder, StandardScaler, OneHotEncoder
from sklearn.covariance import EllipticEnvelope
from sklearn.neighbors import LocalOutlierFactor
from sklearn.feature_selection import f_classif, f_regression, RFE, SelectFromModel, GenericUnivariateSelect
from sklearn.decomposition import PCA

from ml_api.apps.documents.repository import DocumentFileCRUD, DocumentPostgreCRUD


def create_hist_data(df: pd.DataFrame, column_name: str, bins: int) -> List[Dict]:
    ints = df[column_name].value_counts(bins=bins).sort_index().reset_index()
    ints['start'] = ints['index'].apply(lambda x: x.left)
    ints['end'] = ints['index'].apply(lambda x: x.right)
    ints.drop('index', axis=1, inplace=True)
    ints.columns = ['value', 'left', 'right']
    return list(ints.to_dict('index').values())


def create_counts_data(df: pd.DataFrame, column_name: str) -> List[Dict]:
    ints = df[column_name].value_counts(normalize=True).reset_index()
    ints.columns = ['name', 'value']
    return list(ints.to_dict('index').values())


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
            length = len(df)
            pages_count = (length - 1)//rows_on_page + 1
            start_index = (page - 1) * rows_on_page
            stop_index = page * rows_on_page
            if stop_index < length:
                return {'total': pages_count, 'records': df.iloc[start_index:stop_index].to_dict()}
            elif start_index < length:
                return {'total': pages_count, 'records': df.iloc[start_index:].to_dict()}
            else:
                return {'total': pages_count, 'records': pd.DataFrame().to_dict()}
        return None

    def get_document_stat_info(self, filename: str) -> pd.DataFrame:
        if DocumentPostgreCRUD(self._db, self._user).read_document_by_name(filename=filename) is not None:
            df = DocumentFileCRUD(self._user).read_document(filename)
            import io
            buffer = io.StringIO()
            df.info(buf=buffer)
            lines = buffer.getvalue().splitlines()
            df = (pd.DataFrame([x.split() for x in lines[5:-2]], columns=lines[3].split())
                  .drop(['#', 'Count'], axis=1))
            df.columns = ['column_name', 'non_null_count', 'data_type']
            return df.to_dict()
        return None

    def get_document_stat_description(self, filename: str) -> pd.DataFrame:
        if DocumentPostgreCRUD(self._db, self._user).read_document_by_name(filename=filename) is not None:
            df = DocumentFileCRUD(self._user).read_document(filename)
            result = df.describe()
            result.index = ["count", "mean", "std", "min", "first_percentile", "second_percentile",  "third_percentile",
                            "max"]
            return result.to_dict()
        return None

    def get_column_stat_description(self, filename: str, bins: int = 10) -> [str, str]:
        if DocumentPostgreCRUD(self._db, self._user).read_document_by_name(filename=filename) is not None:
            result = []
            df = DocumentFileCRUD(self._user).read_document(filename)
            column_marks = self.read_column_marks(filename)
            for column_name in column_marks['numeric']:
                data = create_hist_data(df=df, column_name=column_name, bins=bins)
                result.append({'name': column_name, 'type': 'numeric', 'data': data})
            for column_name in column_marks['categorical']:
                data = create_counts_data(df=df, column_name=column_name)
                result.append({'name': column_name, 'type': 'categorical', 'data': data})
            column_name = column_marks['target']
            try:
                data = create_hist_data(df=df, column_name=column_name, bins=bins)
                result.append({'name': column_name, 'type': 'numeric', 'data': data})
            except TypeError:
                data = create_counts_data(df=df, column_name=column_name)
                result.append({'name': column_name, 'type': 'categorical', 'data': data})
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

    def update_pipeline(self, filename: str, function_name: str, task_type: str = None,
                        param: Union[int, float, str] = None):
        pipeline = self.read_pipeline(filename)
        if task_type and param:
            pipeline.append([function_name, task_type, param])
        else:
            pipeline.append(function_name)
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

    def validate_column_marks(self, filename: str, target_column: str, task_type: str) -> Dict[str, Union[List, str]]:
        df = DocumentFileCRUD(self._user).read_document(filename)
        numeric_columns = df.select_dtypes('number').columns.values
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.values
        return {
            'numeric': numeric_columns,
            'categorical': categorical_columns,
            'target': target_column,
            'task_type': task_type
        }

    def update_column_marks(self, filename: str, target_column: str, task_type: str):
        column_marks = self.validate_column_marks(filename, target_column, task_type)
        query = {
            'column_marks': column_marks
        }
        DocumentPostgreCRUD(self._db, self._user).update_document(filename, query)

    def apply_pipeline_to_csv(self, filename: str, pipeline: List[Union[str, List]]):
        for function in pipeline:
            if type(function) == List:
                function_name, param = function
                self.apply_function(filename=filename, function_name=function_name, param=param)
            else:
                self.apply_function(filename=filename, function_name=function)

    def copy_and_apply_pipeline_to_another_document(self, filename_orig: str, filename_new: str):
        pipeline = self.read_pipeline(filename_orig)
        self.apply_pipeline_to_csv(filename_new, pipeline)

    def apply_function(self, filename: str, function_name: str, param: Union[int, float, str] = None):
        document = DocumentFileCRUD(self._user).read_document(filename)
        column_marks = self.read_column_marks(filename)
        document_operator = DocumentOperator(document, column_marks)

        if function_name == 'remove_duplicates':
            document_operator.remove_duplicates()
        elif function_name == 'drop_na':
            document_operator.drop_na()
        elif function_name == 'drop_column':
            document_operator.drop_column(column=param)
            self.update_pipeline(filename, function_name='drop_column', task_type=column_marks['task_type'],
                                 param=param)
        elif function_name == 'miss_insert_mean_mode':
            document_operator.miss_insert_mean_mode()
        elif function_name == 'miss_linear_imputer':
            document_operator.miss_linear_imputer()
        elif function_name == 'miss_knn_imputer':
            document_operator.miss_knn_imputer()

        elif function_name == 'standardize_features':
            document_operator.standardize_features()
            self.update_pipeline(filename, function_name='standardize_features')
        elif function_name == 'ordinal_encoding':
            document_operator.ordinal_encoding()
            self.update_pipeline(filename, function_name='ordinal_encoding')
        elif function_name == 'one_hot_encoding':
            document_operator.one_hot_encoding()
            self.update_pipeline(filename, function_name='one_hot_encoding')

        elif function_name == 'outliers_isolation_forest':
            document_operator.outliers_isolation_forest()
        elif function_name == 'outliers_elliptic_envelope':
            document_operator.outliers_elliptic_envelope()
        elif function_name == 'outliers_local_factor':
            document_operator.outliers_local_factor()
        elif function_name == 'outliers_one_class_svm':
            document_operator.outliers_one_class_svm()
        elif function_name == 'outliers_sgd_one_class_svm':
            document_operator.outliers_sgd_one_class_svm()

        elif function_name == 'fs_select_k_best':
            document_operator.fs_generic_univariate_select(mode='k_best', param=param)
            self.update_pipeline(filename, function_name=f'fs_select_k_best', task_type=column_marks['task_type'],
                                 param=param)
        elif function_name == 'fs_select_percentile':
            document_operator.fs_generic_univariate_select(mode='percentile', param=param)
            self.update_pipeline(filename, function_name=f'fs_select_percentile', task_type=column_marks['task_type'],
                                 param=param)
        elif function_name == 'fs_select_fpr':
            document_operator.fs_generic_univariate_select(mode='fpr', param=param)
            self.update_pipeline(filename, function_name=f'fs_select_fpr', task_type=column_marks['task_type'],
                                 param=param)
        elif function_name == 'fs_select_fdr':
            document_operator.fs_generic_univariate_select(mode='fdr', param=param)
            self.update_pipeline(filename, function_name=f'fs_select_fdr', task_type=column_marks['task_type'],
                                 param=param)
        elif function_name == 'fs_select_fwe':
            document_operator.fs_generic_univariate_select(mode='fwe', param=param)
            self.update_pipeline(filename, function_name=f'fs_select_fwe', task_type=column_marks['task_type'],
                                 param=param)
        elif function_name == 'fs_select_rfe':
            document_operator.fs_select_rfe()
            self.update_pipeline(filename, function_name='fs_select_rfe', task_type=column_marks['task_type'],
                                 param=param)
        elif function_name == 'fs_select_from_model':
            document_operator.fs_select_from_model()
            self.update_pipeline(filename, function_name='fs_select_from_model', task_type=column_marks['task_type'],
                                 param=param)
        elif function_name == 'fs_select_pca':
            document_operator.fs_select_pca()
            self.update_pipeline(filename, function_name='fs_select_pca', task_type=column_marks['task_type'],
                                 param=param)

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

    def check_nans(self, columns) -> bool:
        if self.df[columns].isna().sum().sum() > 0:
            return True
        return False

    def check_categorical(self) -> bool:
        if len(self.column_marks['categorical']) > 0:
            return True
        return False

    # CHAPTER 1: MISSING DATA AND DUPLICATES----------------------------------------------------------------------------

    def remove_duplicates(self):
        self.df.drop_duplicates(inplace=True)

    def drop_na(self):
        self.df.dropna(inplace=True)

    def drop_column(self, column: str):
        try:
            self.column_marks['numeric'].remove(column)
        except ValueError:
            try:
                self.column_marks['categorical'].remove(column)
            except ValueError:
                print('Something wrong! def drop_column()')
        self.df.drop(column, axis=1)

    def miss_insert_mean_mode(self):
        numeric_columns = self.column_marks['numeric']
        categorical_columns = self.column_marks['categorical']
        self.df[numeric_columns] = pd.DataFrame(SimpleImputer(strategy='mean').fit_transform(self.df[numeric_columns]),
                                                self.df.index, numeric_columns)
        self.df[categorical_columns] = pd.DataFrame(SimpleImputer(strategy='most_frequent').fit_transform(
                                                    self.df[numeric_columns]), self.df.index, categorical_columns)

    def miss_linear_imputer(self):
        numeric_columns = self.column_marks['numeric']
        self.df[numeric_columns] = pd.DataFrame(IterativeImputer().fit_transform(self.df[numeric_columns]),
                                                self.df.index, numeric_columns)

    def miss_knn_imputer(self):
        numeric_columns = self.column_marks['numeric']
        self.df[numeric_columns] = pd.DataFrame(KNNImputer().fit_transform(self.df[numeric_columns]),
                                                self.df.index, numeric_columns)

    # CHAPTER 2: FEATURE TRANSFORMATION---------------------------------------------------------------------------------
    def standardize_features(self):
        numeric_columns = self.column_marks['numeric']
        if self.check_nans(numeric_columns):
            self.miss_insert_mean_mode()
        sc = StandardScaler()
        self.df[numeric_columns] = pd.DataFrame(sc.fit_transform(self.df[numeric_columns]), self.df.index,
                                                numeric_columns)

    def ordinal_encoding(self):  # не работает на пропусках в данных
        categorical = self.column_marks['categorical']
        if self.check_nans(categorical):
            self.miss_insert_mean_mode()
        self.df[categorical] = OrdinalEncoder().fit_transform(self.df[categorical])

        self.column_marks['numeric'].extend(categorical)
        self.column_marks['categorical'] = []

    def one_hot_encoding(self):
        categorical = self.column_marks['categorical']
        if self.check_nans(categorical):
            self.miss_insert_mean_mode()
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
        if self.check_nans(numeric_columns):
            self.miss_insert_mean_mode()
        outliers = IsolationForest().fit_predict(self.df[numeric_columns])
        self.df = self.df.loc[outliers == 1].reset_index(drop=True)

    def outliers_elliptic_envelope(self):
        numeric_columns = self.column_marks['numeric']
        if self.check_nans(numeric_columns):
            self.miss_insert_mean_mode()
        outliers = EllipticEnvelope().fit_predict(self.df[numeric_columns])
        self.df = self.df.loc[outliers == 1].reset_index(drop=True)

    def outliers_local_factor(self):
        numeric_columns = self.column_marks['numeric']
        if self.check_nans(numeric_columns):
            self.miss_insert_mean_mode()
        outliers = LocalOutlierFactor().fit_predict(self.df[numeric_columns])
        self.df = self.df.loc[outliers == 1].reset_index(drop=True)

    def outliers_one_class_svm(self):
        numeric_columns = self.column_marks['numeric']
        if self.check_nans(numeric_columns):
            self.miss_insert_mean_mode()
        outliers = OneClassSVM().fit_predict(self.df[numeric_columns])
        self.df = self.df.loc[outliers == 1].reset_index(drop=True)

    def outliers_sgd_one_class_svm(self):
        numeric_columns = self.column_marks['numeric']
        if self.check_nans(numeric_columns):
            self.miss_insert_mean_mode()
        outliers = SGDOneClassSVM().fit_predict(self.df[numeric_columns])
        self.df = self.df.loc[outliers == 1].reset_index(drop=True)

    # CANCELLED FOR FIRST ITERATION:
    # def outliers_three_sigma(self):
    # def outliers_grubbs(self):
    # def outliers_approximate(self):
    # def outliers_interquartile_distance(self):

    # CHAPTER 4: FEATURE SELECTION (required: all columns are numeric)--------------------------------------------------

    def fs_generic_univariate_select(self, select_mode: str, param: float = 1e-5):
        # mode: {‘percentile’, ‘k_best’, ‘fpr’, ‘fdr’, ‘fwe’}
        if self.check_categorical():
            self.one_hot_encoding()
        target = self.column_marks['target']
        x, y = self.df.drop(target, axis=1), self.df[target]
        if self.column_marks['task_type'] == 'classification':
            selector = GenericUnivariateSelect(f_classif, mode=select_mode, param=param)
        else:
            selector = GenericUnivariateSelect(f_regression, mode=select_mode, param=param)
        selector.fit(x, y)
        selected_columns = self.df.columns[selector.get_support(indices=True)]
        self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
        self.df[target] = y
        self.column_marks['numeric'] = selected_columns

    def fs_select_rfe(self, param: int = None):
        if self.check_categorical():
            self.one_hot_encoding()
        target = self.column_marks['target']
        x, y = self.df.drop(target, axis=1), self.df[target]
        if self.column_marks['task_type'] == 'classification':
            selector = RFE(LogisticRegression(), n_features_to_select=param)
        else:
            selector = RFE(LinearRegression(), n_features_to_select=param)
        selector.fit(x, y)
        selected_columns = self.df.columns[selector.get_support(indices=True)]
        self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
        self.df[target] = y
        self.column_marks['numeric'] = selected_columns

    def fs_select_from_model(self, param: int = None):
        if self.check_categorical():
            self.one_hot_encoding()
        target = self.column_marks['target']
        x, y = self.df.drop(target, axis=1), self.df[target]
        if self.column_marks['task_type'] == 'classification':
            selector = SelectFromModel(LogisticRegression(), max_features=param)
        else:
            selector = SelectFromModel(LinearRegression(), max_features=param)
        selector.fit(x, y)
        selected_columns = self.df.columns[selector.get_support(indices=True)]
        self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
        self.df[target] = y
        self.column_marks['numeric'] = selected_columns

    def fs_select_pca(self, param: int = None):
        if self.check_categorical():
            self.one_hot_encoding()
        target = self.column_marks['target']
        x, y = self.df.drop(target, axis=1), self.df[target]
        n_components = param
        if n_components is None:
            selector = PCA().fit(x)
            n_components = len(selector.singular_values_[selector.singular_values_ > 1])
        selector = PCA(n_components=n_components)
        selector.fit(x)
        selected_columns = [f'PC{i}' for i in range(1, n_components + 1)]
        self.df = pd.DataFrame(selector.transform(x), columns=selected_columns)
        self.df[target] = y
        self.column_marks['numeric'] = selected_columns

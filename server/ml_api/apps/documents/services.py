import pandas as pd
from datetime import datetime
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

from ml_api.apps.documents.models import Document
from ml_api.apps.documents.repository import DocumentFileCRUD, DocumentPostgreCRUD


class DocumentService:

    def __init__(self, db, user):
        self._db = db
        self._user = user

    def upload_document_to_db(self, file, filename: str):
        DocumentFileCRUD(self._user).upload_document(filename, file)
        DocumentPostgreCRUD(self._db, self._user).new_document(filename)
        pass

    def download_document_from_db(self, filename: str):
        file = DocumentFileCRUD(self._user).download_document(filename)
        return file

    def read_document_from_db(self, filename: str) -> pd.DataFrame:
        df = DocumentFileCRUD(self._user).read_document(filename)
        return df.head(10)

    def rename_document(self, filename: str, new_filename: str):
        DocumentFileCRUD(self._user).rename_document(filename, new_filename)
        query = {
            'name': new_filename
        }
        DocumentPostgreCRUD(self._db, self._user).update_document(filename, query)

    def delete_document_from_db(self, filename: str):
        DocumentFileCRUD(self._user).delete_document(filename)
        DocumentPostgreCRUD(self._db, self._user).delete_document(filename)

    def update_change_date_in_db(self, filename: str):
        query = {
            'change_date': str(datetime.now())
        }
        DocumentPostgreCRUD(self._db, self._user).update_document(filename, query)

    # DOCUMENT CHANGING METHODS
    def remove_duplicates(self, filename: str):
        document = DocumentFileCRUD(self._user).read_document(filename)
        document = document.drop_duplicates()
        DocumentFileCRUD(self._user).update_document(filename, document)
        self.update_change_date_in_db(filename)

    def drop_na(self, filename: str):
        document = DocumentFileCRUD(self._user).read_document(filename)
        document = document.dropna()
        DocumentFileCRUD(self._user).update_document(filename, document)
        self.update_change_date_in_db(filename)

# OCSVM на выходе 1 - выброс, -1 - не выброс
# iter - количество итераций, если -1, то нет ограничений
    def outliers_OneClassSVM(self, filename: str, iters: float):
        df = DocumentFileCRUD(self._user).read_document(filename)
        dataset = df.copy()
        OCSVM = OneClassSVM(kernel='rbf', gamma='auto', max_iter=iters)
        df_with_svm = dataset.join(pd.DataFrame(OCSVM.fit_predict(dataset),
                                                index=dataset.index, columns=['svm']), how='left')
        df = df_with_svm.loc[df_with_svm['svm'] != 1].index
        DocumentFileCRUD(self._user).update_document(filename, df)
        self.update_change_date_in_db(filename)

    def fill_spaces(self):
        pass

    def remove_outlayers(self):
        pass

    def standartize_features(self):
        pass

    def normalize_features(self):
        pass

    # def train_test_split(self):
    #     pass

    def miss_linear_imputer(self, filename: str):
        document = DocumentFileCRUD(self._user).read_document(filename)
        temp_document = pd.DataFrame(IterativeImputer().fit_transform(document)) # default estimator = BayesianRidge()
        temp_document.columns = document.columns
        DocumentFileCRUD(self._user).update_document(filename, temp_document)
        self.update_change_date_in_db(filename)  
import pandas as pd
from datetime import datetime
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

from ml_api.apps.ml_models.models import Model
from ml_api.apps.documents.repository import DocumentFileCRUD
from ml_api.apps.ml_models.repository import ModelPostgreCRUD, ModelPickleCRUD


class ModelService:

    def __init__(self, db, user):
        self._db = db
        self._user = user

    def download_model_from_db(self, model_name: str):
        file = ModelPickleCRUD(self._user).download_pickled_model(model_name)
        return file

    def rename_model(self, model_name: str, new_model_name: str):
        ModelPickleCRUD(self._user).rename_model(model_name, new_model_name)
        query = {
            'name': new_model_name
        }
        ModelPostgreCRUD(self._db, self._user).update_model(model_name, query)

    def delete_model_from_db(self, model_name: str):
        ModelPickleCRUD(self._user).delete_model(model_name)
        ModelPostgreCRUD(self._db, self._user).delete_model(model_name)

    # MODEL TRAINING METHODS

    def get_tree_classifier(self):
        model = DecisionTreeClassifier()
        return model

    def get_document(self, filename: str) -> pd.DataFrame:
        data = DocumentFileCRUD(self._user).read_document(filename)
        return data

    def train_model(self, filename: str, model_name: str = 'tree', split_method: str = 'train/valid'):
        data = self.get_document(filename)
        if split_method == 'train/valid':
            x_train, x_valid, y_train, y_valid = SampleSplitter(data.drop('Species', axis=1), data['Species']).train_valid_split()
        if model_name == 'tree':
            model = self.get_tree_classifier()
        model.fit(x_train, y_train)
        score = model.score(x_valid, y_valid)
        ModelPickleCRUD(self._user).save_model(model_name, model)
        ModelPostgreCRUD(self._db, self._user).new_model(model_name)
        return score

    def predict_on_model(self, filename: str, model_name: str = 'tree'):
        data = self.get_document(filename).iloc[-10:].drop('Species', axis=1)
        model = ModelPickleCRUD(self._user).read_model(model_name)
        predictions = model.predict(data)
        return list(predictions)


class SampleSplitter:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def train_valid_split(self, test_size: float = 0.3):
        return train_test_split(self.x, self.y, test_size=test_size)

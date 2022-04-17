import pandas as pd
from typing import Dict, Union
from datetime import datetime
from sklearn.tree import DecisionTreeClassifier
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from fastapi.responses import JSONResponse
from fastapi import status

from ml_api.apps.ml_models.models import Model
from ml_api.apps.documents.services import DocumentService
from ml_api.apps.ml_models.repository import ModelPostgreCRUD, ModelPickleCRUD
from ml_api.apps.ml_models.configs.classification_models_config import DecisionTreeClassifierParameters, \
    CatBoostClassifierParameters, PythonMLModel, AvailableModels
from ml_api.apps.ml_models.configs.compositions_config import AvailableCompositions

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

    def get_tree_classifier(self, params: DecisionTreeClassifierParameters):
        print(params.dict())
        model = DecisionTreeClassifier(**params.dict())
        return model

    def get_document(self, filename: str) -> pd.DataFrame:
        data = DocumentService(self._db, self._user).read_document_from_db(filename)
        return data

    def train_model(self, filename: str, model: AvailableModels, model_name: str, split_method: str = 'train/valid',
                    params=DecisionTreeClassifierParameters):
        model_info = ModelPostgreCRUD(self._db, self._user).read_model_info(model_name)
        print(model_info)
        if model_info is not None:
            return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content="The model name is already taken")
        data = self.get_document(filename)
        if data is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="No such csv document")

        if split_method == 'train/valid':
            x_train, x_valid, y_train, y_valid = SampleSplitterService(data.drop('Species', axis=1), data['Species']).train_valid_split()

        if model.value == 'DecisionTreeClassifier':
            model = self.get_tree_classifier(params=params)
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


class SampleSplitterService:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def train_valid_split(self, test_size: float = 0.3):
        return train_test_split(self.x, self.y, test_size=test_size)


class CompositionService:

    # def build_composition(self, models: Dict[AvailableModels: PythonMLModel], composition_type: AvailableCompositions):
    #     if composition_type.value == 'simple_voting':
    #         self.build_simple_voting()
    #     if composition_type.value == 'weighted_voting':
    #         self.build_weighted_voting()
    #     if composition_type.value == 'bagging':
    #         self.build_bagging()
    #     if composition_type.value == 'stacking':
    #         self.build_stacking()
    #     print(models)

    def build_simple_voting(self):
        pass

    def build_weighted_voting(self):
        pass

    def build_bagging(self):
        pass

    def build_stacking(self):
        pass

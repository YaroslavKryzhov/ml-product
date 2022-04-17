import pandas as pd
from typing import Dict, Union, Optional, Any
from datetime import datetime
from sklearn.tree import DecisionTreeClassifier
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split, cross_validate
from fastapi.responses import JSONResponse
from fastapi import status
from sklearn.metrics import recall_score, precision_score, f1_score, roc_curve, roc_auc_score, \
accuracy_score, confusion_matrix, precision_recall_curve

from ml_api.apps.ml_models.models import Model
from ml_api.apps.documents.services import DocumentService
from ml_api.apps.ml_models.repository import ModelPostgreCRUD, ModelPickleCRUD
from ml_api.apps.ml_models.configs.classification_models_config import DecisionTreeClassifierParameters, \
    CatBoostClassifierParameters, AvailableModels
from ml_api.apps.ml_models.configs.compositions_config import AvailableCompositions
from ml_api.apps.ml_models.schemas import AvailableSplits
from ml_api.apps.documents.services import DocumentService


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

    def get_catboost_classifier(self, params: CatBoostClassifierParameters):
        print(params.dict())
        model = CatBoostClassifier(**params.dict())
        return model

    def get_document(self, filename: str) -> pd.DataFrame:
        data = DocumentService(self._db, self._user).read_document_from_db(filename)
        return data

    def train_classification_model(self, filename: str, model_type: AvailableModels, model_name: str,
                                   split_type: AvailableSplits,
                                   test_size: Optional[float] = 0.2, cv_groups: Optional[int] = 4,
                                   params=Dict[str, Any]):
        model_info = ModelPostgreCRUD(self._db, self._user).read_model_info(model_name)
        if model_info is not None:
            return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content=f"The model name '{model_info[0]}' "
                                                                                    f"is already taken")

        data = self.get_document(filename)
        if data is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="No such csv document")

        target_column = DocumentService(self._db, self._user).read_column_marks(filename)['target']
        print(target_column)
        features = data.drop(target_column, axis=1)
        target = data[target_column]

        if model_type.value == 'DecisionTreeClassifier':
            model = self.get_tree_classifier(params=DecisionTreeClassifierParameters(**params))
        if model_type.value == 'CatBoostClassifier':
            model = self.get_catboost_classifier(params=CatBoostClassifierParameters(**params))

        metrics = {}
        if split_type.value == 'train/valid':
            x_train, x_valid, y_train, y_valid = train_test_split(features, target, test_size=test_size)
            model.fit(x_train, y_train)
            preds = model.predict(x_valid)
            probs = model.predict_proba(x_valid)[:, 1]
            metrics['accuracy'] = accuracy_score(y_valid, preds)
            metrics['recall'] = recall_score(y_valid, preds)
            metrics['precision'] = precision_score(y_valid, preds)
            metrics['f1'] = f1_score(y_valid, preds)
            metrics['roc_auc'] = roc_auc_score(y_valid, probs)
        if split_type.value == 'cross validation':
            cv_results = cross_validate(model, features, target, cv=cv_groups, scoring=('accuracy', 'recall',
                                                                                        'precision', 'f1', 'roc_auc'))
            metrics['accuracy'] = list(cv_results['test_accuracy'])
            metrics['recall'] = list(cv_results['test_recall'])
            metrics['precision'] = list(cv_results['test_precision'])
            metrics['f1'] = list(cv_results['test_f1'])
            metrics['roc_auc'] = list(cv_results['test_roc_auc'])

        ModelPickleCRUD(self._user).save_model(model_name, model)
        ModelPostgreCRUD(self._db, self._user).new_model(model_name)
        print(metrics)
        return metrics

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

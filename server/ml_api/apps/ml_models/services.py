from typing import Dict, Optional, Any, List
from functools import partial

from sklearn.tree import DecisionTreeClassifier
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split, cross_validate
from fastapi.responses import JSONResponse
from fastapi import status
from sklearn.metrics import recall_score, precision_score, f1_score, roc_auc_score, accuracy_score
from sklearn.ensemble import VotingClassifier, StackingClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from hyperopt import hp, fmin, tpe, Trials, STATUS_OK, space_eval

from ml_api.apps.ml_models.repository import ModelPostgreCRUD, ModelPickleCRUD
from ml_api.apps.ml_models.configs.classification_models_config import DecisionTreeClassifierParameters, \
    CatBoostClassifierParameters, AvailableModels
from ml_api.apps.documents.services import DocumentService
from ml_api.apps.ml_models.configs.classification_searchers_config import CLASSIFICATION_SEARCHERS_CONFIG
from ml_api.apps.ml_models.schemas import ModelWithParams


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

    def train_model(self, task_type: str, composition_type: str,
                    model_params: List[ModelWithParams], params_type: str,
                    document_name: str, model_name: str, test_size: Optional[float] = 0.2):

        model_info = ModelPostgreCRUD(self._db, self._user).read_model_info(model_name)
        if model_info is not None:
            return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content=f"The model name '{model_info[0]}' "
                                                                                    f"is already taken")

        data = DocumentService(self._db, self._user).read_document_from_db(document_name)
        if data is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="No such csv document")

        target_column = DocumentService(self._db, self._user).read_column_marks(document_name)['target']
        features = data.drop(target_column, axis=1)
        target = data[target_column]

        if task_type == 'classification' and target.nunique() == 1:
            return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content="Only one class label in csv")

        print(model_params)
        if params_type == 'auto':
            model_params = AutoParamsSearch(task_type=task_type, model_params=model_params,
                                            features=features, target=target).search_params()

        composition = CompositionConstructor(task_type=task_type, composition_type=composition_type,
                                             models_with_params=model_params).build_composition()

        print(composition)

        model, metrics = CompositionValidator(task_type=task_type, composition=composition, model_name=model_name,
                                              features=features, target=target, test_size=test_size).validate_model()

        ModelPickleCRUD(self._user).save_model(model_name, model)
        ModelPostgreCRUD(self._db, self._user).new_model(model_name)

        return metrics

    # def predict_on_model(self, filename: str, model_name: str = 'tree'):
    #     data = self.get_document(filename).iloc[-10:].drop('Species', axis=1)
    #     model = ModelPickleCRUD(self._user).read_model(model_name)
    #     predictions = model.predict(data)
    #     return list(predictions)


class AutoParamsSearch:

    def __init__(self, task_type, model_params, features, target):
        self.task_type = task_type
        self.model_params = model_params
        self.features = features
        self.target = target

    def search_params(self):
        for i, model_data in enumerate(self.model_params):
            self.model_params[i] = list(model_data[0], self.validate_model_params(model_data[0]))
        return self.model_params

    def validate_model_params(self, model_type: AvailableModels) -> Dict[str, Any]:
        if self.task_type == 'classification':
            search_space = CLASSIFICATION_SEARCHERS_CONFIG.get(model_type.value)
            if self.target.nunique() == 2:
                best = fmin(
                    fn=partial(self.objective_binary, model_type=model_type),
                    space=search_space,
                    algo=tpe.suggest,
                    max_evals=50,
                    show_progressbar=True
                )
                return space_eval(search_space, best)
            else:
                best = fmin(
                    fn=partial(self.objective_multiclass, model_type=model_type),
                    space=search_space,
                    algo=tpe.suggest,
                    max_evals=50,
                    show_progressbar=True
                )
                return space_eval(search_space, best)
        return {}

    def objective_multiclass(self, params, model_type):
        model = ModelConstructor(task_type=self.task_type, model_type=model_type, params=params).model
        skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=1)
        score = cross_val_score(estimator=model, X=self.features, y=self.target,
                                scoring='roc_auc_ovr_weighted', cv=skf, n_jobs=-1, error_score="raise")
        return {'loss': -score.mean(), 'params': params, 'status': STATUS_OK}

    def objective_binary(self, params, model_type):
        model = ModelConstructor(task_type=self.task_type, model_type=model_type, params=params).model
        skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=1)
        score = cross_val_score(estimator=model, X=self.features, y=self.target,
                                scoring='roc_auc', cv=skf, n_jobs=-1, error_score="raise")
        return {'loss': -score.mean(), 'params': params, 'status': STATUS_OK}


    # def objective_regression(self, params, task_type, model_type, features, target):
    #     model = ModelConstructor(task_type=task_type, model_type=model_type, params=params).model
    #     skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=1)
    #     score = cross_val_score(estimator=model, X=features, y=target,
    #                             scoring='roc_auc_ovr_weighted', cv=skf, n_jobs=-1, error_score="raise")
    #
    #     return {'loss': -score.mean(), 'params': params, 'status': STATUS_OK}


class CompositionConstructor:
    """
        Returns sklearn composition model with fit(), predict() methods
    """

    def __init__(self, task_type: str, composition_type: str, models_with_params: Dict[AvailableModels, Dict[str, Any]]):
        self.task_type = task_type
        self.composition_type = composition_type
        self.models_with_params = models_with_params

    def build_composition(self):
        models = []
        if self.composition_type == 'none':
            for model, params in self.models_with_params:
                composition = ModelConstructor(task_type=self.task_type, model_type=model, params=params).model
            return composition
        for model, params in self.models_with_params:
            models.append((model.value, ModelConstructor(task_type=self.task_type, model_type=model, params=params).model))
        if self.composition_type == 'simple_voting':
            composition = VotingClassifier(estimators=models, voting='hard')
            return composition
        elif self.composition_type == 'weighted_voting':
            composition = VotingClassifier(estimators=models, voting='soft')
            return composition
        elif self.composition_type == 'stacking':
            final_estimator = GradientBoostingClassifier()
            composition = StackingClassifier(estimators=models, final_estimator=final_estimator)
            return composition


class ModelConstructor:
    """
        Create sklearn model from hyper-parameters
    """

    def __init__(self, task_type: str, model_type: AvailableModels, params=Dict[str, Any]):
        self.model_type = model_type
        self.params = params
        if task_type == 'classification':
            self.model = self.construct_classification_model()
        # elif task_type == 'regression':
        #     self.model = self.construct_regression_model()

    def construct_classification_model(self):
        if self.model_type.value == 'DecisionTreeClassifier':
            model = self.get_tree_classifier()
            return model
        if self.model_type.value == 'CatBoostClassifier':
            model = self.get_catboost_classifier()
            return model
        return None

    # def construct_regression_model(self):
    #     return None

    def get_tree_classifier(self):
        params = DecisionTreeClassifierParameters(**self.params)
        # print(params.dict())
        model = DecisionTreeClassifier(**params.dict())
        return model

    def get_catboost_classifier(self):
        params = CatBoostClassifierParameters(**self.params)
        # print(params.dict())
        model = CatBoostClassifier(**params.dict())
        return model


class CompositionValidator:

    def __init__(self, task_type, composition, model_name, features, target, test_size):
        self.task_type = task_type
        self.composition = composition
        self.model_name = model_name
        self.features = features
        self.target = target
        self.test_size = test_size

    def validate_model(self):
        if self.task_type == 'classification':
            if self.target.nunique() == 2:
                return self.process_binary_classification()
            else:
                return self.process_multiclass__classification()

    def process_binary_classification(self):
        metrics = {}
        features_train, features_valid, target_train, target_valid = train_test_split(self.features, self.target,
                                                                                      test_size=self.test_size,
                                                                                      stratify=self.target)
        self.composition.fit(features_train, target_train)
        predictions = self.composition.predict(features_valid)
        probabilities = self.composition.predict_proba(features_valid)[:, 1]
        metrics['accuracy'] = accuracy_score(target_valid, predictions)
        metrics['recall'] = recall_score(target_valid, predictions)
        metrics['precision'] = precision_score(target_valid, predictions)
        metrics['f1'] = f1_score(target_valid, predictions)
        metrics['roc_auc'] = roc_auc_score(target_valid, probabilities)

        return self.composition, metrics

    def process_multiclass__classification(self):
        metrics = {}
        features_train, features_valid, target_train, target_valid = train_test_split(self.features, self.target,
                                                                                      test_size=self.test_size,
                                                                                      stratify=self.target)
        self.composition.fit(features_train, target_train)
        predictions = self.composition.predict(features_valid)
        probabilities = self.composition.predict_proba(features_valid)
        metrics['accuracy'] = accuracy_score(target_valid, predictions)
        metrics['recall'] = recall_score(target_valid, predictions, average='weighted')
        metrics['precision'] = precision_score(target_valid, predictions, average='weighted')
        metrics['f1'] = f1_score(target_valid, predictions, average='weighted')
        metrics['roc_auc'] = roc_auc_score(target_valid, probabilities, average='weighted', multi_class='ovr')

        return self.composition, metrics

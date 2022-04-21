from typing import Dict, Optional, Any
from sklearn.tree import DecisionTreeClassifier
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split, cross_validate
from fastapi.responses import JSONResponse
from fastapi import status
from sklearn.metrics import recall_score, precision_score, f1_score, roc_auc_score, accuracy_score
from sklearn.ensemble import VotingClassifier, StackingClassifier, GradientBoostingClassifier

from ml_api.apps.ml_models.repository import ModelPostgreCRUD, ModelPickleCRUD
from ml_api.apps.ml_models.configs.classification_models_config import DecisionTreeClassifierParameters, \
    CatBoostClassifierParameters, AvailableModels
from ml_api.apps.documents.services import DocumentService
from ml_api.apps.ml_models.configs.classification_searchers_config import CLASSIFICATION_SEARCHERS_CONFIG


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
                    model_params: Dict[AvailableModels, Dict[str, Any]], params_type: str,
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

        if params_type == 'auto':
            model_params = AutoParamsSearch(model_params=model_params, features=features, target=target)

        composition = CompositionConstructor(task_type=task_type, composition_type=composition_type,
                                             models_with_params=model_params).build_composition()

        trainer = ModelTrainer(model=composition, model_name=model_name, features=features,
                               target=target, test_size=test_size)

        model, metrics = trainer.process_multiclass_train_split_classification()

        ModelPickleCRUD(self._user).save_model(model_name, model)
        ModelPostgreCRUD(self._db, self._user).new_model(model_name)

        # if target.nunique() == 2:
        #     if split_type.value == 'train/valid':
        #         metrics = trainer.process_binary_train_split_classification(test_size=test_size)
        #     if split_type.value == 'cross validation':
        #         metrics = trainer.process_binary_cross_validate_classification(cv_groups=cv_groups)
        # elif target.nunique() > 2:
        #     if split_type.value == 'train/valid':
        #         metrics = trainer.process_multiclass_train_split_classification(test_size=test_size)
        #     if split_type.value == 'cross validation':
        #         metrics = trainer.process_multiclass_cross_validate_classification(cv_groups=cv_groups)
        # else:
        #     return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content="Only one "
        #                                                                             "target class label in sample")
        return metrics

    # def predict_on_model(self, filename: str, model_name: str = 'tree'):
    #     data = self.get_document(filename).iloc[-10:].drop('Species', axis=1)
    #     model = ModelPickleCRUD(self._user).read_model(model_name)
    #     predictions = model.predict(data)
    #     return list(predictions)


class AutoParamsSearch:

    def __init__(self, model_params, features, target):
        self.model_params = model_params
        self.features = features
        self.target = target

    def search_params(self):
        for model in self.model_params.keys():
            self.model_params[model] = self.validate_model_params(model)

    def validate_model_params(self, model: str) -> Dict[str, Any]:
        search_space = CLASSIFICATION_SEARCHERS_CONFIG.get(model)
        return {}


class CompositionConstructor:
    """
        Returns sklearn composition model with fit(), predict() methods
    """

    def __init__(self, task_type: str, composition_type: str,
                 models_with_params: Dict[AvailableModels: Dict[str, Any]]):
        self.task_type = task_type
        self.composition_type = composition_type
        self.models_with_params = models_with_params

    def build_composition(self):
        models = []
        for model, params in self.models_with_params.items():
            models.append((model, ModelConstructor(task_type=self.task_type, model_type=model, params=params).model))
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
        elif self.composition_type == 'none':
            composition = models[0]
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
        elif task_type == 'regression':
            self.model = self.construct_regression_model()

    def construct_classification_model(self):
        if self.model_type.value == 'DecisionTreeClassifier':
            model = self.get_tree_classifier()
        if self.model_type.value == 'CatBoostClassifier':
            model = self.get_catboost_classifier()
        return model

    def construct_regression_model(self):
        return None

    def get_tree_classifier(self):
        params = DecisionTreeClassifierParameters(**self.params)
        print(params.dict())
        model = DecisionTreeClassifier(**params.dict())
        return model

    def get_catboost_classifier(self):
        params = CatBoostClassifierParameters(**self.params)
        print(params.dict())
        model = CatBoostClassifier(**params.dict())
        return model


class ModelTrainer:

    def __init__(self, model, model_name, features, target, test_size):

        self.model = model
        self.model_name = model_name
        self.features = features
        self.target = target
        self.test_size = test_size

    def process_binary_train_split_classification(self, test_size: int):
        metrics = {}
        features_train, features_valid, target_train, target_valid = train_test_split(self.features, self.target,
                                                                                      test_size=test_size,
                                                                                      stratify=self.target)
        self.model.fit(features_train, target_train)
        predictions = self.model.predict(features_valid)
        probabilities = self.model.predict_proba(features_train)[:, 1]
        metrics['accuracy'] = accuracy_score(target_valid, predictions)
        metrics['recall'] = recall_score(target_valid, predictions)
        metrics['precision'] = precision_score(target_valid, predictions)
        metrics['f1'] = f1_score(target_valid, predictions)
        metrics['roc_auc'] = roc_auc_score(target_valid, probabilities)

        return self.model, metrics

    def process_multiclass_train_split_classification(self, test_size: int):
        metrics = {}
        features_train, features_valid, target_train, target_valid = train_test_split(self.features, self.target,
                                                                                      test_size=test_size,
                                                                                      stratify=self.target)
        self.model.fit(features_train, target_train)
        predictions = self.model.predict(features_valid)
        probabilities = self.model.predict_proba(features_train)[:, 1]
        metrics['accuracy'] = accuracy_score(target_valid, predictions)
        metrics['recall'] = recall_score(target_valid, predictions, average='weighted')
        metrics['precision'] = precision_score(target_valid, predictions, average='weighted')
        metrics['f1'] = f1_score(target_valid, predictions, average='weighted')
        metrics['roc_auc'] = roc_auc_score(target_valid, probabilities, average='weighted')


        return metrics

    def process_binary_cross_validate_classification(self, cv_groups: int):
        metrics = {}
        cv_results = cross_validate(self.model, self.features, self.target, cv=cv_groups, scoring=('accuracy', 'recall',
                                                                                                   'precision', 'f1',
                                                                                                   'roc_auc'))

        metrics['accuracy'] = list(cv_results['test_accuracy'])
        metrics['recall'] = list(cv_results['test_recall'])
        metrics['precision'] = list(cv_results['test_precision'])
        metrics['f1'] = list(cv_results['test_f1'])
        metrics['roc_auc'] = list(cv_results['test_roc_auc'])

        return metrics

    def process_multiclass_cross_validate_classification(self, cv_groups: int):
        metrics = {}
        cv_results = cross_validate(self.model, self.features, self.target, cv=cv_groups, scoring=('accuracy',
                                                                                                   'recall_weighted',
                                                                                                   'precision_weighted',
                                                                                                   'f1_weighted',
                                                                                                   'roc_auc_ovr_weighted'))

        metrics['accuracy'] = list(cv_results['test_accuracy'])
        metrics['recall'] = list(cv_results['test_recall_weighted'])
        metrics['precision'] = list(cv_results['test_precision_weighted'])
        metrics['f1'] = list(cv_results['test_f1_weighted'])
        metrics['roc_auc'] = list(cv_results['test_roc_auc_ovr_weighted'])

        return metrics

from typing import Dict, Optional, Any, List
from functools import partial

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, ExtraTreesClassifier, \
    RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC, LinearSVC
# from catboost import CatBoostClassifier
# from xgboost import XGBClassifier
# from lightgbm import LGBMClassifier

from sklearn.model_selection import train_test_split
from fastapi.responses import JSONResponse
from fastapi import status, BackgroundTasks
from sklearn.metrics import recall_score, precision_score, f1_score, \
    roc_auc_score, accuracy_score, roc_curve, auc
from sklearn.ensemble import VotingClassifier, StackingClassifier, \
    GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from hyperopt import fmin, tpe, STATUS_OK, space_eval
from sklearn.preprocessing import label_binarize
import numpy as np

from ml_api.apps.ml_models.repository import ModelPostgreCRUD, ModelPickleCRUD
import ml_api.apps.ml_models.configs.classification_models as models_config
from ml_api.apps.documents.services import DocumentService
from ml_api.apps.documents.repository import DocumentPostgreCRUD
from ml_api.apps.ml_models.configs.classification_searchers import \
    CLASSIFICATION_SEARCHERS_CONFIG
from ml_api.apps.ml_models.schemas import CompositionParams, \
    MulticlassClassificationMetrics, BinaryClassificationMetrics, \
    CompositionReport, CompositionFullInfoResponse, \
    CompositionShortInfoResponse


class ModelService:

    def __init__(self, db, user):
        self._db = db
        self._user = user

    def read_model_info(self, model_name: str) -> CompositionFullInfoResponse:
        model_info = ModelPostgreCRUD(self._db, self._user).read_by_name(
            model_name=model_name)
        csv_name = DocumentPostgreCRUD(self._db, self._user).read_by_uuid(
            model_info.csv_id)
        model_info = CompositionFullInfoResponse(csv_name=csv_name,
                                                 **model_info.dict())
        return model_info

    def read_models_info(self) -> List[CompositionShortInfoResponse]:
        result = []
        models = ModelPostgreCRUD(self._db, self._user).read_all()
        for model in models:
            csv_name = DocumentPostgreCRUD(self._db, self._user).read_by_uuid(
                model.csv_id)
            result.append(CompositionShortInfoResponse(csv_name=csv_name,
                                                       **model.dict()))
        return models

    def download_model(self, model_name: str):
        file = ModelPickleCRUD(self._user).download_pickled(model_name)
        return file

    def rename_model(self, model_name: str, new_model_name: str):
        ModelPickleCRUD(self._user).rename(model_name, new_model_name)
        query = {
            'name': new_model_name
        }
        ModelPostgreCRUD(self._db, self._user).update(model_name, query)

    def delete_model(self, model_name: str):
        ModelPostgreCRUD(self._db, self._user).delete(model_name)
        ModelPickleCRUD(self._user).delete(model_name)

    def train_model(self,
                    task_type: str,
                    composition_type: str,
                    composition_params: List[CompositionParams],
                    params_type: str,
                    document_name: str,
                    model_name: str,
                    background_tasks: BackgroundTasks,
                    test_size: Optional[float] = 0.2):

        error = self.check_errors_in_input(document_name=document_name,
            model_name=model_name, composition_type=composition_type,
            composition_params=composition_params)
        if error:
            return error

        document_id = DocumentService(
            self._db, self._user).read_document_info(filename=document_name).id

        data = DocumentService(self._db, self._user)._read_document(
            document_name)
        target_column = DocumentService(
            self._db, self._user).read_column_types(document_name).target
        features = data.drop(target_column, axis=1)
        features_names = features.columns.to_list()
        target = data[target_column]

        # checks if classification sample is wrong
        if task_type == 'classification' and target.nunique() == 1:
            return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                content="Only one class label in csv")

        # create model in db
        ModelPostgreCRUD(self._db, self._user).create(model_name=model_name,
            csv_id=str(document_id), task_type=task_type,
            features=features_names, target=target_column,
            composition_type=composition_type, composition_params=None,
            stage='Training', report=None)

        # start training task
        background_tasks.add_task(self._validate_training, document_name,
            features, target, task_type, composition_type, composition_params,
            params_type, model_name, test_size)

        return JSONResponse(status_code=status.HTTP_200_OK,
            content=f"Training of model '{model_name}' starts at background")

    def check_errors_in_input(self,
                              document_name: str,
                              model_name: str,
                              composition_type: str,
                              composition_params: List[CompositionParams]
                              ) -> bool:
        # checks if name is available
        model_info = ModelPostgreCRUD(self._db, self._user).read_by_name(
            model_name=model_name)
        if model_info:
            return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                content=f"The model name '{model_info.name}' is taken")

        # checks if data exists
        document_info = DocumentService(
            self._db, self._user).read_document_info(filename=document_name)
        if document_info is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content="No such csv document")

        # checks composition settings
        if composition_type == 'none' and len(composition_params) > 1:
            return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                content="If composition type is 'NONE' should be one model")
        return False

    def _validate_training(self,
                           document_name: str,
                           features,
                           target,
                           task_type: str,
                           composition_type: str,
                           composition_params: List[CompositionParams],
                           params_type: str,
                           model_name: str,
                           test_size: Optional[float] = 0.2):
        if params_type == 'auto':
            composition_params = AutoParamsSearch(task_type=task_type,
                composition_params=composition_params, features=features,
                target=target).search_params()

        composition = CompositionConstructor(task_type=task_type,
            composition_type=composition_type,
            models_with_params=composition_params).build_composition()

        model, metrics = CompositionValidator(task_type=task_type,
            composition=composition, model_name=model_name, features=features,
            target=target, test_size=test_size).validate_model()

        report = CompositionReport(csv_name=document_name,
            metrics=metrics)

        self._save_model(model_name=model_name, model=model, report=report,
            composition_params=composition_params)

    def _save_model(self,
                    model_name: str,
                    model,
                    composition_params: List[CompositionParams],
                    report):
        query = {
            'composition_params': composition_params,
            'stage': 'Trained',
            'report': report,
        }
        ModelPickleCRUD(self._user).save(model_name, model)
        ModelPostgreCRUD(self._db, self._user).update(model_name=model_name,
            query=query)

    def predict_on_model(self, filename: str, model_name: str):
        features = DocumentService(self._db, self._user)._read_document(
            filename)
        model_info = ModelPostgreCRUD(self._db, self._user).read_by_name(
            model_name=model_name)
        print(features.columns.to_list())
        print(model_info.features)
        if features.columns.to_list() != model_info.features:
            return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                content="Features in doc and in model training history are "
                "different")
        model = ModelPickleCRUD(self._user).load(model_name)
        predictions = model.predict(features)
        return {"predictions": list(predictions)}


class AutoParamsSearch:

    def __init__(self,
                 task_type: str,
                 composition_params: List[CompositionParams],
                 features,
                 target):
        self.task_type = task_type
        self.composition_params = composition_params
        self.features = features
        self.target = target

    def search_params(self):
        for i, model_data in enumerate(self.composition_params):
            self.composition_params[i].params = self._validate_params(
                model_data.type)
        return self.composition_params

    def _validate_params(self,
                         model_type: models_config.AvailableModels
                         ) -> Dict[str, Any]:
        # to bo: add regression
        if self.task_type == 'classification':
            search_space = CLASSIFICATION_SEARCHERS_CONFIG.get(
                model_type.value)
            if self.target.nunique() == 2:
                best = fmin(
                    fn=partial(self._objective_binary,
                               model_type=model_type),
                    space=search_space,
                    algo=tpe.suggest,
                    max_evals=50,
                    show_progressbar=True
                )
                return space_eval(search_space, best)
            else:
                best = fmin(
                    fn=partial(self._objective_multiclass,
                               model_type=model_type),
                    space=search_space,
                    algo=tpe.suggest,
                    max_evals=50,
                    show_progressbar=True
                )
                return space_eval(search_space, best)
        return {}

    def _objective_binary(self, params,
                          model_type: models_config.AvailableModels):
        """
            Auxiliary function for scoring of checking iterating parameters.
            Binary classification task type.

            :param params: checking parameters;
            :param model_type: AvailableModels type string model name;
            :return: dict(loss, params, status)
        """
        model = ModelConstructor(task_type=self.task_type,
            model_type=model_type, params=params).model
        skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=1)
        score = cross_val_score(estimator=model, X=self.features,
            y=self.target, scoring='roc_auc', cv=skf, n_jobs=-1,
            error_score="raise")
        return {'loss': -score.mean(), 'params': params, 'status': STATUS_OK}

    def _objective_multiclass(self, params,
                              model_type: models_config.AvailableModels):
        """
            Auxiliary function for scoring of checking iterating parameters.
            Multiclass classification task type.

            :param params: checking parameters;
            :param model_type: AvailableModels type string model name;
            :return: dict(loss, params, status)
        """
        model = ModelConstructor(task_type=self.task_type,
            model_type=model_type, params=params).model
        skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=1)
        score = cross_val_score(estimator=model, X=self.features,
            y=self.target, scoring='roc_auc_ovr_weighted', cv=skf, n_jobs=-1,
            error_score="raise")
        return {'loss': -score.mean(), 'params': params, 'status': STATUS_OK}

    # def objective_regression(self, params, task_type, model_type, features,
    #                          target):
    #     model = ModelConstructor(task_type=task_type, model_type=model_type,
    #         params=params).model
    #     skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=1)
    #     score = cross_val_score(estimator=model, X=features, y=target,
    #                             scoring='roc_auc_ovr_weighted', cv=skf,
    #                             n_jobs=-1, error_score="raise")
    #
    #     return {'loss': -score.mean(), 'params': params, 'status': STATUS_OK}


class ModelConstructor:
    """CLASS READY, ADD MODELS, not logic methods, add regression
        Create sklearn estimator from hyper-parameters
    """

    def __init__(self,
                 task_type: str,
                 model_type: models_config.AvailableModels,
                 params=Dict[str, Any]):
        self.model_type = model_type
        self.params = params
        if task_type == 'classification':
            self.model = self._construct_classification_model()
        # elif task_type == 'regression':
        #     self.model = self._construct_regression_model()

        decision_tree = 'DecisionTreeClassifier'
        random_forest = 'RandomForestClassifier'
        # catboost = 'CatBoostClassifier'
        adaboost = 'AdaBoostClassifier'
        gradient_boosting = 'GradientBoostingClassifier'
        bagging = "BaggingClassifier"
        extra_trees = "ExtraTreesClassifier"
        SGD = "SGDClassifier"
        linear_SVC = "LinearSVC"
        SVC = "SVC"
        logistic_regression = 'LogisticRegression'
        perceptron = 'MLPClassifier'

    def _construct_classification_model(self):
        if self.model_type.value == 'DecisionTreeClassifier':
            model = self._get_tree_classifier()
            return model
        # if self.model_type.value == 'CatBoostClassifier':
        #     model = self._get_catboost_classifier()
        #     return model
        if self.model_type.value == 'RandomForestClassifier':
            model = self._get_forest_classifier()
            return model
        if self.model_type.value == 'AdaBoostClassifier':
            model = self._get_adaboost_classifier()
            return model
        if self.model_type.value == 'GradientBoostingClassifier':
            model = self._get_gradient_boosting_classifier()
            return model
        if self.model_type.value == 'BaggingClassifier':
            model = self._get_bagging_classifier()
            return model
        if self.model_type.value == 'ExtraTreesClassifier':
            model = self._get_extra_trees_classifier()
            return model
        if self.model_type.value == 'SGDClassifier':
            model = self._get_sgd_classifier()
            return model
        if self.model_type.value == 'LinearSVC':
            model = self._get_linear_svc_classifier()
            return model
        if self.model_type.value == 'SVC':
            model = self._get_sgd_classifier()
            return model
        if self.model_type.value == 'LogisticRegression':
            model = self._get_log_reg_classifier()
            return model
        if self.model_type.value == 'MLPClassifier':
            model = self._get_mlp_classifier()
            return model
        return None

    # def construct_regression_model(self):
    #     return None

    def _get_tree_classifier(self):
        params = models_config.DecisionTreeClassifierParameters(**self.params)
        model = DecisionTreeClassifier(**params.dict())
        return model

    # def _get_catboost_classifier(self):
    #     params = models_config.CatBoostClassifierParameters(**self.params)
    #     model = CatBoostClassifier(**params.dict())
    #     return model

    def _get_forest_classifier(self):
        params = models_config.RandomForestClassifierParameters(**self.params)
        model = RandomForestClassifier(**params.dict())
        return model

    def _get_adaboost_classifier(self):
        params = models_config.AdaBoostClassifierParameters(**self.params)
        model = AdaBoostClassifier(**params.dict())
        return model

    def _get_gradient_boosting_classifier(self):
        params = models_config.GradientBoostingClassifierParameters(**self.params)
        model = GradientBoostingClassifier(**params.dict())
        return model

    def _get_bagging_classifier(self):
        params = models_config.BaggingClassifierParameters(**self.params)
        model = BaggingClassifier(**params.dict())
        return model

    def _get_extra_trees_classifier(self):
        params = models_config.ExtraTreesClassifierParameters(**self.params)
        model = ExtraTreesClassifier(**params.dict())
        return model

    def _get_sgd_classifier(self):
        params = models_config.SGDClassifierParameters(**self.params)
        model = SGDClassifier(**params.dict())
        return model

    def _get_linear_svc_classifier(self):
        params = models_config.LinearSVCParameters(**self.params)
        model = LinearSVC(**params.dict())
        return model

    def _get_svc_classifier(self):
        params = models_config.SVCParameters(**self.params)
        model = SVC(**params.dict())
        return model

    def _get_log_reg_classifier(self):
        params = models_config.LogisticRegressionParameters(**self.params)
        model = LogisticRegression(**params.dict())
        return model

    def _get_mlp_classifier(self):
        params = models_config.MLPClassifierParameters(**self.params)
        model = MLPClassifier(**params.dict())
        return model

    # def _get_xgb_classifier(self):
    #     params = models_config.XGBClassifierParameters(**self.params)
    #     model = XGBClassifier(**params.dict())
    #     return model
    #
    # def _get_lgbm_classifier(self):
    #     params = models_config.LGBMClassifierParameters(**self.params)
    #     model = LGBMClassifier(**params.dict())
    #     return model


class CompositionConstructor:
    """CLASS IS READY, add regression
    Creates sklearn composition/model with fit(), predict() methods
    Uses ModelConstructor class for component estimators"""

    def __init__(self,
                 task_type: str,
                 composition_type: str,
                 models_with_params: List[CompositionParams]):
        """
        :param task_type: one of ml_models.schemas.AvailableTaskTypes
        :param composition_type: one of ml_models.schemas.AvailableCompositions
        :param models_with_params: list of ml_models.schemas.CompositionParams
        """
        self.task_type = task_type
        self.composition_type = composition_type
        self.models_with_params = models_with_params

    def build_composition(self):
        """
        Creates composition for CompositionValidator class.
        If composition_type is 'none' returns sklearn model;
        If 'simple_voting' - VotingClassifier without weights;
        If 'weighted_voting' - VotingClassifier with weights;
        If 'stacking' - StackingClassifier with GradientBoosting on head;
        :return:
        sklearn estimator
        """
        models = []
        if self.composition_type == 'none':
            model = self.models_with_params[0]
            composition = ModelConstructor(task_type=self.task_type,
                model_type=model.type, params=model.params).model
            return composition
        for i, model in enumerate(self.models_with_params):
            models.append((str(i) + "_" + model.type.value, ModelConstructor(
                task_type=self.task_type, model_type=model.type,
                params=model.params).model))
        if self.composition_type == 'simple_voting':
            composition = VotingClassifier(estimators=models, voting='hard')
            return composition
        elif self.composition_type == 'weighted_voting':
            composition = VotingClassifier(estimators=models, voting='soft')
            return composition
        elif self.composition_type == 'stacking':
            final_estimator = GradientBoostingClassifier()
            composition = StackingClassifier(estimators=models,
                final_estimator=final_estimator)
            return composition


class CompositionValidator:
    """
    add regression
    """

    def __init__(self,
                 task_type,
                 composition,
                 model_name,
                 features,
                 target,
                 test_size):
        self.task_type = task_type
        self.composition = composition
        self.model_name = model_name
        self.features = features
        self.target = target
        self.test_size = test_size

    def validate_model(self):
        if self.task_type == 'classification':
            if self.target.nunique() == 2:
                return self._process_binary_classification()
            else:
                return self._process_multiclass__classification()

    def _process_binary_classification(self):
        features_train, features_valid, target_train, target_valid = \
            train_test_split(self.features, self.target,
            test_size=self.test_size, stratify=self.target)
        self.composition.fit(features_train, target_train)
        predictions = self.composition.predict(features_valid)
        try:
            probabilities = self.composition.predict_proba(
                features_valid)[:, 1]
        except AttributeError:
            try:
                probabilities = self.composition.decision_function(features_valid)
            except AttributeError:
                probabilities = False
                
        roc_auc = None
        fpr = None
        tpr = None

        accuracy = accuracy_score(target_valid, predictions)
        recall = recall_score(target_valid, predictions)
        precision = precision_score(target_valid, predictions)
        f1 = f1_score(target_valid, predictions)
        if probabilities:
            roc_auc = roc_auc_score(target_valid, probabilities)
            fpr, tpr, _ = roc_curve(target_valid, probabilities)
            fpr = list(fpr)
            tpr = list(tpr)
        report = BinaryClassificationMetrics(accuracy=accuracy, recall=recall,
            precision=precision, f1=f1, roc_auc=roc_auc, fpr=fpr, tpr=tpr)
        return self.composition, report

    def _process_multiclass__classification(self):
        features_train, features_valid, target_train, target_valid = \
            train_test_split(self.features, self.target,
                test_size=self.test_size, stratify=self.target)
        self.composition.fit(features_train, target_train)
        predictions = self.composition.predict(features_valid)
        try:
            probabilities = self.composition.predict_proba(features_valid)
        except AttributeError:
            try:
                probabilities = self.composition.decision_function(features_valid)
            except AttributeError:
                probabilities = False

        accuracy = accuracy_score(target_valid, predictions)
        recall = recall_score(target_valid, predictions,
            average='weighted')
        precision = precision_score(target_valid, predictions,
            average='weighted')
        f1 = f1_score(target_valid, predictions, average='weighted')

        roc_auc_weighted = None
        roc_auc_micro = None
        roc_auc_macro = None
        fpr_micro = None
        fpr_macro = None
        tpr_micro = None
        tpr_macro = None

        if probabilities:
            classes = list(self.target.unique())
            target_valid = label_binarize(target_valid, classes=classes)
            n_classes = len(classes)

            roc_auc_weighted = roc_auc_score(target_valid,
                probabilities, average='weighted', multi_class='ovr')

            fpr = dict()
            tpr = dict()
            roc_auc = dict()

            for i in range(n_classes):
                fpr[i], tpr[i], _ = roc_curve(target_valid[:, i],
                    probabilities[:, i])
                roc_auc[i] = auc(fpr[i], tpr[i])

            fpr["micro"], tpr["micro"], _ = roc_curve(target_valid.ravel(),
                probabilities.ravel())
            roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

            # First aggregate all false positive rates
            all_fpr = np.unique(np.concatenate([fpr[i] for i in
                range(n_classes)]))

            # Then interpolate all ROC curves at this points
            mean_tpr = np.zeros_like(all_fpr)
            for i in range(n_classes):
                mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])

            # Finally average it and compute AUC
            mean_tpr /= n_classes

            fpr["macro"] = all_fpr
            tpr["macro"] = mean_tpr
            roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

            fpr_micro = list(fpr["micro"])
            tpr_micro = list(tpr["micro"])
            fpr_macro = list(fpr["macro"])
            tpr_macro = list(tpr["macro"])
            roc_auc_micro = roc_auc["micro"]
            roc_auc_macro = roc_auc["macro"]

        report = MulticlassClassificationMetrics(accuracy=accuracy,
            recall=recall, precision=precision, f1=f1,
            roc_auc_weighted=roc_auc_weighted, roc_auc_micro=roc_auc_micro,
            roc_auc_macro=roc_auc_macro, fpr_micro=fpr_micro,
            fpr_macro=fpr_macro, tpr_micro=tpr_micro, tpr_macro=tpr_macro)
        return self.composition, report

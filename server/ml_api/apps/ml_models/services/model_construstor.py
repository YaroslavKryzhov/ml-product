from typing import Dict, Any, Callable

from sklearn import linear_model, tree, svm, ensemble, neural_network, \
    neighbors

from ml_api.apps.ml_models.utils import classification_models_params
from ml_api.apps.ml_models import specs


class CreateModelException(Exception):
    pass


class ModelConstructor:

    def __init__(
            self,
            task_type: specs.AvailableTaskTypes,
            model_type: specs.AvailableModelTypes,
            params=Dict[str, Any],
    ):
        self.task_type = task_type
        self.model_type = model_type
        self.params = params
        self._models_map: Dict[specs.AvailableModelTypes, Callable] = {
            specs.AvailableModelTypes.decision_tree: self._get_tree_classifier,
            specs.AvailableModelTypes.random_forest: self._get_forest_classifier,
            specs.AvailableModelTypes.adaboost: self._get_adaboost_classifier,
            specs.AvailableModelTypes.gradient_boosting: self._get_gradient_boosting_classifier,
            specs.AvailableModelTypes.bagging: self._get_bagging_classifier,
            specs.AvailableModelTypes.extra_trees: self._get_extra_trees_classifier,
            specs.AvailableModelTypes.SGD: self._get_sgd_classifier,
            specs.AvailableModelTypes.linear_SVC: self._get_linear_svc_classifier,
            specs.AvailableModelTypes.SVC: self._get_sgd_classifier,
            specs.AvailableModelTypes.logistic_regression: self._get_log_reg_classifier,
            specs.AvailableModelTypes.perceptron: self._get_mlp_classifier,
            specs.AvailableModelTypes.k_neighbors: self._get_k_neighbors_classifier,
            # TODO: add regression models to utils/regression_models_params
        }

    def get_model(self):
        if self.task_type == specs.AvailableTaskTypes.CLASSIFICATION:
            return self._construct_classification_model()
        elif self.task_type == specs.AvailableTaskTypes.REGRESSION:
            return self._construct_regression_model()
        else:
            raise CreateModelException(
                f'Unknown task type: {self.task_type}')

    def _no_model_error(self):
        raise CreateModelException(
            'Unknown model: Model not found in ModelConstructor.models_map')

    def _construct_classification_model(self):
        get_model = self._models_map.get(self.model_type, self._no_model_error)
        return get_model()

    def _get_tree_classifier(self):
        params = classification_models_params.DecisionTreeClassifierParameters(
            **self.params)
        model = tree.DecisionTreeClassifier(**params.dict())
        return model

    def _get_forest_classifier(self):
        params = classification_models_params.RandomForestClassifierParameters(
            **self.params)
        model = ensemble.RandomForestClassifier(**params.dict())
        return model

    def _get_adaboost_classifier(self):
        params = classification_models_params.AdaBoostClassifierParameters(
            **self.params)
        model = ensemble.AdaBoostClassifier(**params.dict())
        return model

    def _get_gradient_boosting_classifier(self):
        params = classification_models_params.GradientBoostingClassifierParameters(
            **self.params
        )
        model = ensemble.GradientBoostingClassifier(**params.dict())
        return model

    def _get_bagging_classifier(self):
        params = classification_models_params.BaggingClassifierParameters(
            **self.params)
        model = ensemble.BaggingClassifier(**params.dict())
        return model

    def _get_extra_trees_classifier(self):
        params = classification_models_params.ExtraTreesClassifierParameters(
            **self.params)
        model = ensemble.ExtraTreesClassifier(**params.dict())
        return model

    def _get_sgd_classifier(self):
        params = classification_models_params.SGDClassifierParameters(
            **self.params)
        model = linear_model.SGDClassifier(**params.dict())
        return model

    def _get_linear_svc_classifier(self):
        params = classification_models_params.LinearSVCParameters(
            **self.params)
        model = svm.LinearSVC(**params.dict())
        return model

    def _get_svc_classifier(self):
        params = classification_models_params.SVCParameters(**self.params)
        model = svm.SVC(**params.dict())
        return model

    def _get_log_reg_classifier(self):
        params = classification_models_params.LogisticRegressionParameters(
            **self.params)
        model = linear_model.LogisticRegression(**params.dict())
        return model

    def _get_mlp_classifier(self):
        params = classification_models_params.MLPClassifierParameters(
            **self.params)
        model = neural_network.MLPClassifier(**params.dict())
        return model

    def _get_k_neighbors_classifier(self):
        params = classification_models_params.KNeighborsClassifierParameters(
            **self.params)
        model = neighbors.KNeighborsClassifier(**params.dict())
        return model

    # def _get_catboost_classifier(self):
    #     params = classification_models_params.CatBoostClassifierParameters(**self.params)
    #     model = CatBoostClassifier(**params.dict())
    #     return model
    # TODO: add boosting: cat/xgb/lgbm
    # def _get_xgb_classifier(self):
    #     params = classification_models_params.XGBClassifierParameters(**self.params)
    #     model = XGBClassifier(**params.dict())
    #     return model
    #
    # def _get_lgbm_classifier(self):
    #     params = classification_models_params.LGBMClassifierParameters(**self.params)
    #     model = LGBMClassifier(**params.dict())
    #     return model

    def _construct_regression_model(self):
        # TODO: add regression models constructor
        raise NotImplementedError

    # TODO: add regression models getters

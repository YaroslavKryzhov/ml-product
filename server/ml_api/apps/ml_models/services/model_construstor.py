from typing import Dict, Any, Callable

from sklearn import tree, ensemble, svm, linear_model, neighbors, \
    naive_bayes, neural_network
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier

from ml_api.apps.ml_models import specs, schemas, errors


class ModelConstructorService:
    # TODO: finish models list in constructor for all tasks
    def __init__(self):
        self._classification_models_map: Dict[specs.AvailableModelTypes, Callable] = {
            specs.AvailableModelTypes.DECISION_TREE_CLASSIFIER: self._get_decision_tree_classifier,
            specs.AvailableModelTypes.RANDOM_FOREST_CLASSIFIER: self._get_random_forest_classifier,
            specs.AvailableModelTypes.EXTRA_TREES_CLASSIFIER: self._get_extra_trees_classifier,
            specs.AvailableModelTypes.GRADIENT_BOOSTING_CLASSIFIER: self._get_gradient_boosting_classifier,
            specs.AvailableModelTypes.ADABOOST_CLASSIFIER: self._get_adaboost_classifier,
            specs.AvailableModelTypes.BAGGING_CLASSIFIER: self._get_bagging_classifier,
            specs.AvailableModelTypes.XGB_CLASSIFIER: self._get_xgb_classifier,
            specs.AvailableModelTypes.LGBM_CLASSIFIER: self._get_lgbm_classifier,
            specs.AvailableModelTypes.CAT_BOOST_CLASSIFIER: self._get_cat_boost_classifier,
            specs.AvailableModelTypes.SGD_CLASSIFIER: self._get_sgd_classifier,
            specs.AvailableModelTypes.LINEAR_SVC: self._get_linear_svc,
            specs.AvailableModelTypes.SVC: self._get_svc,
            specs.AvailableModelTypes.LOGISTIC_REGRESSION: self._get_logistic_regression,
            specs.AvailableModelTypes.PASSIVE_AGGRESSIVE_CLASSIFIER: self._get_passive_aggressive_classifier,
            specs.AvailableModelTypes.K_NEIGHBORS_CLASSIFIER: self._get_k_neighbors_classifier,
            specs.AvailableModelTypes.RADIUS_NEIGHBORS_CLASSIFIER: self._get_radius_neighbors_classifier,
            specs.AvailableModelTypes.MLP_CLASSIFIER: self._get_mlp_classifier,
        }
        self._regression_models_map: Dict[
            specs.AvailableModelTypes, Callable] = {
            specs.AvailableModelTypes.DECISION_TREE_REGRESSOR: self._get_decision_tree_regressor,
            specs.AvailableModelTypes.RANDOM_FOREST_REGRESSOR: self._get_random_forest_regressor,
            specs.AvailableModelTypes.EXTRA_TREES_REGRESSOR: self._get_extra_trees_regressor,
            specs.AvailableModelTypes.GRADIENT_BOOSTING_REGRESSOR: self._get_gradient_boosting_regressor,
            specs.AvailableModelTypes.ADABOOST_REGRESSOR: self._get_adaboost_regressor,
            specs.AvailableModelTypes.BAGGING_REGRESSOR: self._get_bagging_regressor,
            specs.AvailableModelTypes.XGB_REGRESSOR: self._get_xgb_regressor,
            specs.AvailableModelTypes.LGBM_REGRESSOR: self._get_lgbm_regressor,
            specs.AvailableModelTypes.CAT_BOOST_REGRESSOR: self._get_cat_boost_regressor,
            specs.AvailableModelTypes.SGD_REGRESSOR: self._get_sgd_regressor,
            specs.AvailableModelTypes.LINEAR_SVR: self._get_linear_svr,
            specs.AvailableModelTypes.SVR: self._get_svr,
            specs.AvailableModelTypes.LINEAR_REGRESSION: self._get_linear_regression,
            specs.AvailableModelTypes.RIDGE: self._get_ridge,
            specs.AvailableModelTypes.LASSO: self._get_lasso,
            specs.AvailableModelTypes.ELASTIC_NET: self._get_elastic_net,
            specs.AvailableModelTypes.PASSIVE_AGGRESSIVE_REGRESSOR: self._get_passive_aggressive_regressor,
            specs.AvailableModelTypes.K_NEIGHBORS_REGRESSOR: self._get_k_neighbors_regressor,
            specs.AvailableModelTypes.RADIUS_NEIGHBORS_REGRESSOR: self._get_radius_neighbors_regressor,
            specs.AvailableModelTypes.MLP_REGRESSOR: self._get_mlp_regressor,
        }

    async def get_model(self, task_type: specs.AvailableTaskTypes,
                  model_params: schemas.ModelParams):
        if task_type == specs.AvailableTaskTypes.CLASSIFICATION:
            model = await self.get_classification_model(model_params)
        elif task_type == specs.AvailableTaskTypes.REGRESSION:
            model = await self.get_regression_model(model_params)
        elif task_type == specs.AvailableTaskTypes.CLUSTERING:
            model = await self.get_clustering_model(model_params)
        elif task_type == specs.AvailableTaskTypes.OUTLIER_DETECTION:
            model = await self.get_outlier_detection_model(model_params)
        elif task_type == specs.AvailableTaskTypes.DIMENSIONALITY_REDUCTION:
            model = await self.get_dimensionality_reduction_model(model_params)
        else:
            raise errors.UnknownTaskTypeError(task_type)
        return model

    async def get_classification_model(self, model_params: schemas.ModelParams):
        classification_model = model_params.model_type
        if classification_model not in self._classification_models_map:
            raise errors.UnknownClassificationModelError(classification_model)
        return self._classification_models_map[classification_model](
            model_params.params)

    def _get_decision_tree_classifier(self, model_params: Dict[str, Any]):
        return tree.DecisionTreeClassifier(**model_params)

    def _get_random_forest_classifier(self, model_params: Dict[str, Any]):
        return ensemble.RandomForestClassifier(**model_params)

    def _get_extra_trees_classifier(self, model_params: Dict[str, Any]):
        return ensemble.ExtraTreesClassifier(**model_params)

    def _get_gradient_boosting_classifier(self, model_params: Dict[str, Any]):
        return ensemble.GradientBoostingClassifier(**model_params)

    def _get_adaboost_classifier(self, model_params: Dict[str, Any]):
        return ensemble.AdaBoostClassifier(**model_params)

    def _get_bagging_classifier(self, model_params: Dict[str, Any]):
        return ensemble.BaggingClassifier(**model_params)

    def _get_xgb_classifier(self, model_params: Dict[str, Any]):
        return XGBClassifier(**model_params)

    def _get_lgbm_classifier(self, model_params: Dict[str, Any]):
        return LGBMClassifier(**model_params)

    def _get_cat_boost_classifier(self, model_params: Dict[str, Any]):
        return CatBoostClassifier(**model_params)

    def _get_sgd_classifier(self, model_params: Dict[str, Any]):
        return linear_model.SGDClassifier(**model_params)

    def _get_linear_svc(self, model_params: Dict[str, Any]):
        return svm.LinearSVC(**model_params)

    def _get_svc(self, model_params: Dict[str, Any]):
        return svm.SVC(**model_params)

    def _get_logistic_regression(self, model_params: Dict[str, Any]):
        return linear_model.LogisticRegression(**model_params)

    def _get_passive_aggressive_classifier(self, model_params: Dict[str, Any]):
        return linear_model.PassiveAggressiveClassifier(**model_params)

    def _get_k_neighbors_classifier(self, model_params: Dict[str, Any]):
        return neighbors.KNeighborsClassifier(**model_params)

    def _get_radius_neighbors_classifier(self, model_params: Dict[str, Any]):
        return neighbors.RadiusNeighborsClassifier(**model_params)

    def _get_mlp_classifier(self, model_params: Dict[str, Any]):
        return neural_network.MLPClassifier(**model_params)

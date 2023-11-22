import traceback
from typing import Dict, Any, Callable

from sklearn import ensemble, linear_model, svm, neighbors, neural_network, \
    tree, cluster, mixture, decomposition, discriminant_analysis, manifold, covariance
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor
from catboost import CatBoostClassifier, CatBoostRegressor

from ml_api.apps.ml_models import specs, schemas, errors
from ml_api.apps.ml_models.specs import AvailableModelTypes as Models
from ml_api.apps.ml_models.specs import AvailableTaskTypes as TaskTypes


class ModelConstructorService:
    """
    Отвечает за сборку sklearn-модели с указанными параметрами.
    """
    def __init__(self):
        self._classification_models_map: Dict[Models, Callable] = {
            Models.DECISION_TREE_CLASSIFIER: self._get_decision_tree_classifier,
            Models.RANDOM_FOREST_CLASSIFIER: self._get_random_forest_classifier,
            Models.EXTRA_TREES_CLASSIFIER: self._get_extra_trees_classifier,
            Models.GRADIENT_BOOSTING_CLASSIFIER: self._get_gradient_boosting_classifier,
            Models.ADABOOST_CLASSIFIER: self._get_adaboost_classifier,
            Models.BAGGING_CLASSIFIER: self._get_bagging_classifier,
            Models.XGB_CLASSIFIER: self._get_xgb_classifier,
            Models.LGBM_CLASSIFIER: self._get_lgbm_classifier,
            Models.CATBOOST_CLASSIFIER: self._get_catboost_classifier,
            Models.SGD_CLASSIFIER: self._get_sgd_classifier,
            Models.LINEAR_SVC: self._get_linear_svc,
            Models.SVC: self._get_svc,
            Models.LOGISTIC_REGRESSION: self._get_logistic_regression,
            Models.PASSIVE_AGGRESSIVE_CLASSIFIER: self._get_passive_aggressive_classifier,
            Models.KNEIGHBORS_CLASSIFIER: self._get_k_neighbors_classifier,
            Models.RADIUS_NEIGHBORS_CLASSIFIER: self._get_radius_neighbors_classifier,
            Models.MLP_CLASSIFIER: self._get_mlp_classifier,
        }
        self._regression_models_map: Dict[Models, Callable] = {
            Models.DECISION_TREE_REGRESSOR: self._get_decision_tree_regressor,
            Models.RANDOM_FOREST_REGRESSOR: self._get_random_forest_regressor,
            Models.EXTRA_TREES_REGRESSOR: self._get_extra_trees_regressor,
            Models.GRADIENT_BOOSTING_REGRESSOR: self._get_gradient_boosting_regressor,
            Models.ADABOOST_REGRESSOR: self._get_adaboost_regressor,
            Models.BAGGING_REGRESSOR: self._get_bagging_regressor,
            Models.XGB_REGRESSOR: self._get_xgb_regressor,
            Models.LGBM_REGRESSOR: self._get_lgbm_regressor,
            Models.CATBOOST_REGRESSOR: self._get_catboost_regressor,
            Models.SGD_REGRESSOR: self._get_sgd_regressor,
            Models.LINEAR_SVR: self._get_linear_svr,
            Models.SVR: self._get_svr,
            Models.LINEAR_REGRESSION: self._get_linear_regression,
            Models.RIDGE: self._get_ridge,
            Models.LASSO: self._get_lasso,
            Models.ELASTIC_NET: self._get_elastic_net,
            Models.PASSIVE_AGGRESSIVE_REGRESSOR: self._get_passive_aggressive_regressor,
            Models.K_NEIGHBORS_REGRESSOR: self._get_k_neighbors_regressor,
            Models.RADIUS_NEIGHBORS_REGRESSOR: self._get_radius_neighbors_regressor,
            Models.MLP_REGRESSOR: self._get_mlp_regressor,
        }

        self._clustering_models_map: Dict[Models, Callable] = {
            Models.KMEANS: self._get_kmeans,
            Models.MINI_BATCH_KMEANS: self._get_mini_batch_kmeans,
            Models.AFFINITY_PROPAGATION: self._get_affinity_propagation,
            Models.MEAN_SHIFT: self._get_mean_shift,
            Models.SPECTRAL_CLUSTERING: self._get_spectral_clustering,
            Models.AGGLOMERATIVE_CLUSTERING: self._get_agglomerative_clustering,
            Models.DBSCAN: self._get_dbscan,
            Models.OPTICS: self._get_optics,
            Models.BIRCH: self._get_birch,
            Models.GAUSSIAN_MIXTURE: self._get_gaussian_mixture,
        }

        self._outlier_detection_models_map: Dict[Models, Callable] = {
            Models.ONE_CLASS_SVM: self._get_one_class_svm,
            Models.SGD_ONE_CLASS_SVM: self._get_sgd_one_class_svm,
            Models.ELLIPTIC_ENVELOPE: self._get_elliptic_envelope,
            Models.LOCAL_OUTLIER_FACTOR: self._get_local_outlier_factor,
            Models.ISOLATION_FOREST: self._get_isolation_forest,
        }

        self._dimensionality_reduction_models_map: Dict[Models, Callable] = {
            Models.PCA: self._get_pca,
            Models.LINEAR_DISCRIMINANT_ANALYSIS: self._get_linear_discriminant_analysis,
            Models.TSNE: self._get_tsne,
            Models.ISOMAP: self._get_isomap,
            Models.NMF: self._get_nmf,
            Models.TRUNCATED_SVD: self._get_truncated_svd,
        }

        self._task_to_models_map_map = {
            TaskTypes.CLASSIFICATION: self._classification_models_map,
            TaskTypes.REGRESSION: self._regression_models_map,
            TaskTypes.CLUSTERING: self._clustering_models_map,
            TaskTypes.OUTLIER_DETECTION: self._outlier_detection_models_map,
            TaskTypes.DIMENSIONALITY_REDUCTION: self._dimensionality_reduction_models_map,
        }

        self._task_to_model_error_map = {
            TaskTypes.CLASSIFICATION: errors.UnknownClassificationModelError,
            TaskTypes.REGRESSION: errors.UnknownRegressionModelError,
            TaskTypes.CLUSTERING: errors.UnknownClusteringModelError,
            TaskTypes.OUTLIER_DETECTION: errors.UnknownOutlierDetectionModelError,
            TaskTypes.DIMENSIONALITY_REDUCTION: errors.UnknownDimensionalityReductionModelError,
        }

    def get_model(self, task_type: specs.AvailableTaskTypes,
                  model_params: schemas.ModelParams):
        model_type = model_params.model_type

        if task_type not in self._task_to_models_map_map:
            raise errors.UnknownTaskTypeError(task_type.value)
        model_map = self._task_to_models_map_map[task_type]

        if model_type not in model_map:
            unknown_model_err = self._task_to_model_error_map[task_type]
            raise unknown_model_err(model_type)
        try:
            model = model_map[model_type](model_params.params)
        except Exception as err:
            # print(traceback.format_exc())
            error_type = type(err).__name__
            error_description = str(err)
            raise errors.ModelConstructionError(f"{error_type}: {error_description}")
        return model

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
        return XGBClassifier(**model_params, verbosity=0)

    def _get_lgbm_classifier(self, model_params: Dict[str, Any]):
        return LGBMClassifier(**model_params, verbosity=-1)

    def _get_catboost_classifier(self, model_params: Dict[str, Any]):
        return CatBoostClassifier(**model_params, verbose=0)

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

    # Regression Models
    def _get_decision_tree_regressor(self, model_params: Dict[str, Any]):
        return tree.DecisionTreeRegressor(**model_params)

    def _get_random_forest_regressor(self, model_params: Dict[str, Any]):
        return ensemble.RandomForestRegressor(**model_params)

    def _get_extra_trees_regressor(self, model_params: Dict[str, Any]):
        return ensemble.ExtraTreesRegressor(**model_params)

    def _get_gradient_boosting_regressor(self, model_params: Dict[str, Any]):
        return ensemble.GradientBoostingRegressor(**model_params)

    def _get_adaboost_regressor(self, model_params: Dict[str, Any]):
        return ensemble.AdaBoostRegressor(**model_params)

    def _get_bagging_regressor(self, model_params: Dict[str, Any]):
        return ensemble.BaggingRegressor(**model_params)

    def _get_xgb_regressor(self, model_params: Dict[str, Any]):
        return XGBRegressor(**model_params, verbosity=0)

    def _get_lgbm_regressor(self, model_params: Dict[str, Any]):
        return LGBMRegressor(**model_params, verbosity=-1)

    def _get_catboost_regressor(self, model_params: Dict[str, Any]):
        return CatBoostRegressor(**model_params, verbose=0)

    def _get_sgd_regressor(self, model_params: Dict[str, Any]):
        return linear_model.SGDRegressor(**model_params)

    def _get_linear_svr(self, model_params: Dict[str, Any]):
        return svm.LinearSVR(**model_params)

    def _get_svr(self, model_params: Dict[str, Any]):
        return svm.SVR(**model_params)

    def _get_linear_regression(self, model_params: Dict[str, Any]):
        return linear_model.LinearRegression(**model_params)

    def _get_ridge(self, model_params: Dict[str, Any]):
        return linear_model.Ridge(**model_params)

    def _get_lasso(self, model_params: Dict[str, Any]):
        return linear_model.Lasso(**model_params)

    def _get_elastic_net(self, model_params: Dict[str, Any]):
        return linear_model.ElasticNet(**model_params)

    def _get_passive_aggressive_regressor(self, model_params: Dict[str, Any]):
        return linear_model.PassiveAggressiveRegressor(**model_params)

    def _get_k_neighbors_regressor(self, model_params: Dict[str, Any]):
        return neighbors.KNeighborsRegressor(**model_params)

    def _get_radius_neighbors_regressor(self, model_params: Dict[str, Any]):
        return neighbors.RadiusNeighborsRegressor(**model_params)

    def _get_mlp_regressor(self, model_params: Dict[str, Any]):
        return neural_network.MLPRegressor(**model_params)

    # Clustering Models
    def _get_kmeans(self, model_params: Dict[str, Any]):
        return cluster.KMeans(**model_params)

    def _get_mini_batch_kmeans(self, model_params: Dict[str, Any]):
        return cluster.MiniBatchKMeans(**model_params)

    def _get_affinity_propagation(self, model_params: Dict[str, Any]):
        return cluster.AffinityPropagation(**model_params)

    def _get_mean_shift(self, model_params: Dict[str, Any]):
        return cluster.MeanShift(**model_params)

    def _get_spectral_clustering(self, model_params: Dict[str, Any]):
        return cluster.SpectralClustering(**model_params)

    def _get_agglomerative_clustering(self, model_params: Dict[str, Any]):
        return cluster.AgglomerativeClustering(**model_params)

    def _get_dbscan(self, model_params: Dict[str, Any]):
        return cluster.DBSCAN(**model_params)

    def _get_optics(self, model_params: Dict[str, Any]):
        return cluster.OPTICS(**model_params)

    def _get_birch(self, model_params: Dict[str, Any]):
        return cluster.Birch(**model_params)

    def _get_gaussian_mixture(self, model_params: Dict[str, Any]):
        return mixture.GaussianMixture(**model_params)

    # Anomaly Detection Models
    def _get_one_class_svm(self, model_params: Dict[str, Any]):
        return svm.OneClassSVM(**model_params)

    def _get_sgd_one_class_svm(self, model_params: Dict[str, Any]):
        return linear_model.SGDOneClassSVM(**model_params)

    def _get_elliptic_envelope(self, model_params: Dict[str, Any]):
        return covariance.EllipticEnvelope(**model_params)

    def _get_local_outlier_factor(self, model_params: Dict[str, Any]):
        return neighbors.LocalOutlierFactor(**model_params)

    def _get_isolation_forest(self, model_params: Dict[str, Any]):
        return ensemble.IsolationForest(**model_params)

    # Dimensionality Reduction Models
    def _get_pca(self, model_params: Dict[str, Any]):
        return decomposition.PCA(**model_params)

    def _get_linear_discriminant_analysis(self, model_params: Dict[str, Any]):
        return discriminant_analysis.LinearDiscriminantAnalysis(**model_params)

    def _get_tsne(self, model_params: Dict[str, Any]):
        return manifold.TSNE(**model_params)

    def _get_isomap(self, model_params: Dict[str, Any]):
        return manifold.Isomap(**model_params)

    def _get_nmf(self, model_params: Dict[str, Any]):
        return decomposition.NMF(**model_params)

    def _get_truncated_svd(self, model_params: Dict[str, Any]):
        return decomposition.TruncatedSVD(**model_params)

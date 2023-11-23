from typing import Dict, Any

from pydantic import ValidationError

from ml_api.apps.ml_models import specs, schemas, errors
from ml_api.apps.ml_models.specs import AvailableModelTypes as Models
from ml_api.apps.ml_models.specs import AvailableTaskTypes as TaskTypes
from ml_api.apps.ml_models.model import ModelMetadata
from ml_api.apps.ml_models.services.processors.params_searcher import HyperoptService
from ml_api.apps.ml_models.models_specs.validation_params import \
    clustering_models_params as cluster_params, \
    classification_models_params as classif_params, \
    dimensionality_reduction_models_params as dim_red_params, \
    outlier_detection_models_params as outl_params, \
    regression_models_params as regr_params


class ParamsValidationService:
    """
    Отвечает за валидацию параметров модели.
    """
    def __init__(self, user_id, model_meta: ModelMetadata):
        self._user_id = user_id
        self.dataframe_id = model_meta.dataframe_id
        self.model_type = model_meta.model_params.model_type
        self.model_params = model_meta.model_params.params
        self.params_type = model_meta.params_type
        self.task_type = model_meta.task_type

        self._classification_models_params_map = {
            Models.DECISION_TREE_CLASSIFIER: classif_params.DecisionTreeClassifierParams,
            Models.RANDOM_FOREST_CLASSIFIER: classif_params.RandomForestClassifierParams,
            Models.EXTRA_TREES_CLASSIFIER: classif_params.ExtraTreesClassifierParams,
            Models.GRADIENT_BOOSTING_CLASSIFIER: classif_params.GradientBoostingClassifierParams,
            Models.ADABOOST_CLASSIFIER: classif_params.AdaBoostClassifierParams,
            Models.BAGGING_CLASSIFIER: classif_params.BaggingClassifierParams,
            Models.XGB_CLASSIFIER: classif_params.XGBClassifierParams,
            Models.LGBM_CLASSIFIER: classif_params.LGBMClassifierParams,
            Models.CATBOOST_CLASSIFIER: classif_params.CatBoostClassifierParams,
            Models.SGD_CLASSIFIER: classif_params.SGDClassifierParams,
            Models.LINEAR_SVC: classif_params.LinearSVCParams,
            Models.SVC: classif_params.SVCParams,
            Models.LOGISTIC_REGRESSION: classif_params.LogisticRegressionParams,
            Models.PASSIVE_AGGRESSIVE_CLASSIFIER: classif_params.PassiveAggressiveClassifierParams,
            Models.KNEIGHBORS_CLASSIFIER: classif_params.KNeighborsClassifierParams,
            Models.RADIUS_NEIGHBORS_CLASSIFIER: classif_params.RadiusNeighborsClassifierParams,
            Models.MLP_CLASSIFIER: classif_params.MLPClassifierParams,
        }

        self._regression_models_params_map = {
            Models.DECISION_TREE_REGRESSOR: regr_params.DecisionTreeRegressorParams,
            Models.RANDOM_FOREST_REGRESSOR: regr_params.RandomForestRegressorParams,
            Models.EXTRA_TREES_REGRESSOR: regr_params.ExtraTreesRegressorParams,
            Models.GRADIENT_BOOSTING_REGRESSOR: regr_params.GradientBoostingRegressorParams,
            Models.ADABOOST_REGRESSOR: regr_params.AdaBoostRegressorParams,
            Models.BAGGING_REGRESSOR: regr_params.BaggingRegressorParams,
            Models.XGB_REGRESSOR: regr_params.XGBRegressorParams,
            Models.LGBM_REGRESSOR: regr_params.LGBMRegressorParams,
            Models.CATBOOST_REGRESSOR: regr_params.CatBoostRegressorParams,
            Models.SGD_REGRESSOR: regr_params.SGDRegressorParams,
            Models.LINEAR_SVR: regr_params.LinearSVRParams,
            Models.SVR: regr_params.SVRParams,
            Models.LINEAR_REGRESSION: regr_params.LinearRegressionParams,
            Models.RIDGE: regr_params.RidgeParams,
            Models.LASSO: regr_params.LassoParams,
            Models.ELASTIC_NET: regr_params.ElasticNetParams,
            Models.PASSIVE_AGGRESSIVE_REGRESSOR: regr_params.PassiveAggressiveRegressorParams,
            Models.K_NEIGHBORS_REGRESSOR: regr_params.KNeighborsRegressorParams,
            Models.RADIUS_NEIGHBORS_REGRESSOR: regr_params.RadiusNeighborsRegressorParams,
            Models.MLP_REGRESSOR: regr_params.MLPRegressorParams,
        }

        self._clustering_models_params_map = {
            Models.KMEANS: cluster_params.KMeansParams,
            Models.MINI_BATCH_KMEANS: cluster_params.MiniBatchKMeansParams,
            Models.AFFINITY_PROPAGATION: cluster_params.AffinityPropagationParams,
            Models.MEAN_SHIFT: cluster_params.MeanShiftParams,
            Models.SPECTRAL_CLUSTERING: cluster_params.SpectralClusteringParams,
            Models.WARD: cluster_params.WardParams,
            Models.AGGLOMERATIVE_CLUSTERING: cluster_params.AgglomerativeClusteringParams,
            Models.DBSCAN: cluster_params.DBSCANParams,
            Models.OPTICS: cluster_params.OPTICSParams,
            Models.BIRCH: cluster_params.BirchParams,
            Models.GAUSSIAN_MIXTURE: cluster_params.GaussianMixtureParams
        }

        self._outlier_detection_models_params_map = {
            Models.ONE_CLASS_SVM: outl_params.OneClassSVMParams,
            Models.SGD_ONE_CLASS_SVM: outl_params.SGDOneClassSVMParams,
            Models.ELLIPTIC_ENVELOPE: outl_params.EllipticEnvelopeParams,
            Models.LOCAL_OUTLIER_FACTOR: outl_params.LocalOutlierFactorParams,
            Models.ISOLATION_FOREST: outl_params.IsolationForestParams
        }

        self._dimensionality_reduction_models_params_map = {
            Models.PCA: dim_red_params.PCAParams,
            Models.LINEAR_DISCRIMINANT_ANALYSIS: dim_red_params.LinearDiscriminantAnalysisParams,
            Models.TSNE: dim_red_params.TSNEParams,
            Models.ISOMAP: dim_red_params.IsomapParams,
            Models.NMF: dim_red_params.NMFParams,
            Models.TRUNCATED_SVD: dim_red_params.TruncatedSVDParams
        }

        self._task_to_models_params_map_map = {
            TaskTypes.CLASSIFICATION: self._classification_models_params_map,
            TaskTypes.REGRESSION: self._regression_models_params_map,
            TaskTypes.CLUSTERING: self._clustering_models_params_map,
            TaskTypes.OUTLIER_DETECTION: self._outlier_detection_models_params_map,
            TaskTypes.DIMENSIONALITY_REDUCTION: self._dimensionality_reduction_models_params_map,
        }

        self._task_to_model_error_map = {
            TaskTypes.CLASSIFICATION: errors.UnknownClassificationModelError,
            TaskTypes.REGRESSION: errors.UnknownRegressionModelError,
            TaskTypes.CLUSTERING: errors.UnknownClusteringModelError,
            TaskTypes.OUTLIER_DETECTION: errors.UnknownOutlierDetectionModelError,
            TaskTypes.DIMENSIONALITY_REDUCTION: errors.UnknownDimensionalityReductionModelError,
        }

    def validate_params(self) -> schemas.ModelParams:
        initial_params = self._get_initial_params()

        validated_params = self._validate_params(initial_params)

        return schemas.ModelParams(model_type=self.model_type,
                                   params=validated_params)

    def _get_initial_params(self) -> Dict:

        if self.params_type == specs.AvailableParamsTypes.DEFAULT:
            return {}
        if self.params_type == specs.AvailableParamsTypes.CUSTOM:
            return self.model_params
        if self.params_type == specs.AvailableParamsTypes.HYPEROPT:
            hyperopt_model_params = HyperoptService(self._user_id, self.dataframe_id
                ).search_params(self.task_type, self.model_type)
            return hyperopt_model_params.params
        raise errors.UnknownParamsTypeError(self.params_type)

    def _validate_params(self, initial_params: Dict) -> Dict[str, Any]:
        if self.task_type not in self._task_to_models_params_map_map:
            raise errors.UnknownTaskTypeError(self.task_type.value)
        model_params_map = self._task_to_models_params_map_map[self.task_type]

        if self.model_type not in model_params_map:
            unknown_model_err = self._task_to_model_error_map[self.task_type]
            raise unknown_model_err(self.model_type)
        model_params_class = model_params_map[self.model_type]

        try:
            validated_params = model_params_class(**initial_params)
        except ValidationError as err:
            raise errors.ModelParamsValidationError(
                self.model_type.value, initial_params, str(err))
        return validated_params.dict()

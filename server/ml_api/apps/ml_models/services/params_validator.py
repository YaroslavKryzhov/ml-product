from typing import Dict, Any

from pydantic import ValidationError

from ml_api.apps.ml_models import specs, schemas, errors
from ml_api.apps.ml_models.services.params_searcher import HyperoptService
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
    def __init__(self):

        self._classification_models_params_map = {
            specs.AvailableModelTypes.DECISION_TREE_CLASSIFIER: classif_params.DecisionTreeClassifierParams,
            specs.AvailableModelTypes.RANDOM_FOREST_CLASSIFIER: classif_params.RandomForestClassifierParams,
            specs.AvailableModelTypes.EXTRA_TREES_CLASSIFIER: classif_params.ExtraTreesClassifierParams,
            specs.AvailableModelTypes.GRADIENT_BOOSTING_CLASSIFIER: classif_params.GradientBoostingClassifierParams,
            specs.AvailableModelTypes.ADABOOST_CLASSIFIER: classif_params.AdaBoostClassifierParams,
            specs.AvailableModelTypes.BAGGING_CLASSIFIER: classif_params.BaggingClassifierParams,
            specs.AvailableModelTypes.XGB_CLASSIFIER: classif_params.XGBClassifierParams,
            specs.AvailableModelTypes.LGBM_CLASSIFIER: classif_params.LGBMClassifierParams,
            specs.AvailableModelTypes.CAT_BOOST_CLASSIFIER: classif_params.CatBoostClassifierParams,
            specs.AvailableModelTypes.SGD_CLASSIFIER: classif_params.SGDClassifierParams,
            specs.AvailableModelTypes.LINEAR_SVC: classif_params.LinearSVCParams,
            specs.AvailableModelTypes.SVC: classif_params.SVCParams,
            specs.AvailableModelTypes.LOGISTIC_REGRESSION: classif_params.LogisticRegressionParams,
            specs.AvailableModelTypes.PASSIVE_AGGRESSIVE_CLASSIFIER: classif_params.PassiveAggressiveClassifierParams,
            specs.AvailableModelTypes.K_NEIGHBORS_CLASSIFIER: classif_params.KNeighborsClassifierParams,
            specs.AvailableModelTypes.RADIUS_NEIGHBORS_CLASSIFIER: classif_params.RadiusNeighborsClassifierParams,
            specs.AvailableModelTypes.MLP_CLASSIFIER: classif_params.MLPClassifierParams,
        }

        self._regression_models_params_map = {
            specs.AvailableModelTypes.DECISION_TREE_REGRESSOR: regr_params.DecisionTreeRegressorParams,
            specs.AvailableModelTypes.RANDOM_FOREST_REGRESSOR: regr_params.RandomForestRegressorParams,
            specs.AvailableModelTypes.EXTRA_TREES_REGRESSOR: regr_params.ExtraTreesRegressorParams,
            specs.AvailableModelTypes.GRADIENT_BOOSTING_REGRESSOR: regr_params.GradientBoostingRegressorParams,
            specs.AvailableModelTypes.ADABOOST_REGRESSOR: regr_params.AdaBoostRegressorParams,
            specs.AvailableModelTypes.BAGGING_REGRESSOR: regr_params.BaggingRegressorParams,
            specs.AvailableModelTypes.XGB_REGRESSOR: regr_params.XGBRegressorParams,
            specs.AvailableModelTypes.LGBM_REGRESSOR: regr_params.LGBMRegressorParams,
            specs.AvailableModelTypes.CAT_BOOST_REGRESSOR: regr_params.CatBoostRegressorParams,
            specs.AvailableModelTypes.SGD_REGRESSOR: regr_params.SGDRegressorParams,
            specs.AvailableModelTypes.LINEAR_SVR: regr_params.LinearSVRParams,
            specs.AvailableModelTypes.SVR: regr_params.SVRParams,
            specs.AvailableModelTypes.LINEAR_REGRESSION: regr_params.LinearRegressionParams,
            specs.AvailableModelTypes.RIDGE: regr_params.RidgeParams,
            specs.AvailableModelTypes.LASSO: regr_params.LassoParams,
            specs.AvailableModelTypes.ELASTIC_NET: regr_params.ElasticNetParams,
            specs.AvailableModelTypes.PASSIVE_AGGRESSIVE_REGRESSOR: regr_params.PassiveAggressiveRegressorParams,
            specs.AvailableModelTypes.K_NEIGHBORS_REGRESSOR: regr_params.KNeighborsRegressorParams,
            specs.AvailableModelTypes.RADIUS_NEIGHBORS_REGRESSOR: regr_params.RadiusNeighborsRegressorParams,
            specs.AvailableModelTypes.MLP_REGRESSOR: regr_params.MLPRegressorParams,
        }

        self._clustering_models_params_map = {
            specs.AvailableModelTypes.K_MEANS: cluster_params.KMeansParams,
            specs.AvailableModelTypes.MINI_BATCH_KMEANS: cluster_params.MiniBatchKMeansParams,
            specs.AvailableModelTypes.AFFINITY_PROPAGATION: cluster_params.AffinityPropagationParams,
            specs.AvailableModelTypes.MEAN_SHIFT: cluster_params.MeanShiftParams,
            specs.AvailableModelTypes.SPECTRAL_CLUSTERING: cluster_params.SpectralClusteringParams,
            specs.AvailableModelTypes.WARD: cluster_params.WardParams,
            specs.AvailableModelTypes.AGGLOMERATIVE_CLUSTERING: cluster_params.AgglomerativeClusteringParams,
            specs.AvailableModelTypes.DBSCAN: cluster_params.DBSCANParams,
            specs.AvailableModelTypes.OPTICS: cluster_params.OPTICSParams,
            specs.AvailableModelTypes.BIRCH: cluster_params.BirchParams,
            specs.AvailableModelTypes.GAUSSIAN_MIXTURE: cluster_params.GaussianMixtureParams
        }

        self._outlier_detection_models_params_map = {
            specs.AvailableModelTypes.ONE_CLASS_SVM: outl_params.OneClassSVMParams,
            specs.AvailableModelTypes.SGD_ONE_CLASS_SVM: outl_params.SGDOneClassSVMParams,
            specs.AvailableModelTypes.ELLIPTIC_ENVELOPE: outl_params.EllipticEnvelopeParams,
            specs.AvailableModelTypes.LOCAL_OUTLIER_FACTOR: outl_params.LocalOutlierFactorParams,
            specs.AvailableModelTypes.ISOLATION_FOREST: outl_params.IsolationForestParams
        }

        self._dimensionality_reduction_models_params_map = {
            specs.AvailableModelTypes.PCA: dim_red_params.PCAParams,
            specs.AvailableModelTypes.LINEAR_DISCRIMINANT_ANALYSIS: dim_red_params.LinearDiscriminantAnalysisParams,
            specs.AvailableModelTypes.T_SNE: dim_red_params.TSNEParams,
            specs.AvailableModelTypes.ISOMAP: dim_red_params.IsomapParams,
            specs.AvailableModelTypes.NMF: dim_red_params.NMFParams,
            specs.AvailableModelTypes.TRUNCATED_SVD: dim_red_params.TruncatedSVDParams
        }

        self._task_to_models_params_map = {
            specs.AvailableTaskTypes.CLASSIFICATION: self._classification_models_params_map,
            specs.AvailableTaskTypes.REGRESSION: self._regression_models_params_map,
            specs.AvailableTaskTypes.CLUSTERING: self._clustering_models_params_map,
            specs.AvailableTaskTypes.OUTLIER_DETECTION: self._outlier_detection_models_params_map,
            specs.AvailableTaskTypes.DIMENSIONALITY_REDUCTION: self._dimensionality_reduction_models_params_map,
        }

        self._task_to_model_error_map = {
            specs.AvailableTaskTypes.CLASSIFICATION: errors.UnknownClassificationModelError,
            specs.AvailableTaskTypes.REGRESSION: errors.UnknownRegressionModelError,
            specs.AvailableTaskTypes.CLUSTERING: errors.UnknownClusteringModelError,
            specs.AvailableTaskTypes.OUTLIER_DETECTION: errors.UnknownOutlierDetectionModelError,
            specs.AvailableTaskTypes.DIMENSIONALITY_REDUCTION: errors.UnknownDimensionalityReductionModelError,
        }

    async def validate_params(self, task_type: specs.AvailableTaskTypes,
                        model_params: schemas.ModelParams,
                        params_type: specs.AvailableParamsTypes,
                        dataframe_info: schemas.DataframeGetterInfo) -> schemas.ModelParams:
        if params_type == specs.AvailableParamsTypes.DEFAULT:
            params = {}
        elif params_type == specs.AvailableParamsTypes.CUSTOM:
            try:
                params = await self._validate_model_params(task_type, model_params)
            except ValidationError as err:
                raise errors.ModelParamsValidationError(model_params, err)
        elif params_type == specs.AvailableParamsTypes.AUTO:
            model_type = model_params.model_type
            model_params = await HyperoptService(dataframe_info).search_params(
                task_type, model_type)
            try:
                params = await self._validate_model_params(task_type, model_params)
            except ValidationError as err:
                raise errors.HyperoptModelParamsValidationError(model_params, err)
        else:
            raise errors.UnknownParamsTypeError(params_type)
        return schemas.ModelParams(type=model_params.model_type, params=params)

    async def _validate_model_params(self, task_type, model_params) -> Dict[str, Any]:
        model_type = model_params.model_type

        if task_type not in self._task_to_models_params_map:
            raise errors.UnknownTaskTypeError(task_type)
        model_params_map = self._task_to_models_params_map[task_type]

        if model_type not in model_params_map:
            unknown_model_err = self._task_to_model_error_map[task_type]
            raise unknown_model_err(model_type)
        model_params_class = model_params_map[model_type]

        # try:
        validated_params = model_params_class(**model_params.params)
        # TODO: move ValidationError raise here after hyperopt debug
        # except ValidationError as err:
        #     raise errors.ModelParamsValidationError(model_params, err)
        return validated_params.dict()

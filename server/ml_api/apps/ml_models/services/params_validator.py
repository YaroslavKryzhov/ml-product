from typing import Dict, Any

from beanie import PydanticObjectId
from pydantic import ValidationError

from ml_api.apps.ml_models import specs, schemas, errors
from ml_api.apps.ml_models.services.params_searcher import HyperortService
from ml_api.apps.ml_models.models_specs import classification_models_params as cl_params


class ParamsValidationService:
    # TODO: finish this class
    """
    Отвечает за валидацию параметров модели.
    """
    def __init__(self):
        self._classification_models_params_map = {
            specs.AvailableModelTypes.DECISION_TREE_CLASSIFIER: cl_params.DecisionTreeClassifierParams,
            specs.AvailableModelTypes.RANDOM_FOREST_CLASSIFIER: cl_params.RandomForestClassifierParams,
            specs.AvailableModelTypes.EXTRA_TREES_CLASSIFIER: cl_params.ExtraTreesClassifierParams,
            specs.AvailableModelTypes.GRADIENT_BOOSTING_CLASSIFIER: cl_params.GradientBoostingClassifierParams,
            specs.AvailableModelTypes.ADABOOST_CLASSIFIER: cl_params.AdaBoostClassifierParams,
            specs.AvailableModelTypes.BAGGING_CLASSIFIER: cl_params.BaggingClassifierParams,
            specs.AvailableModelTypes.XGB_CLASSIFIER: cl_params.XGBClassifierParams,
            specs.AvailableModelTypes.LGBM_CLASSIFIER: cl_params.LGBMClassifierParams,
            specs.AvailableModelTypes.CAT_BOOST_CLASSIFIER: cl_params.CatBoostClassifierParams,
            specs.AvailableModelTypes.SGD_CLASSIFIER: cl_params.SGDClassifierParams,
            specs.AvailableModelTypes.LINEAR_SVC: cl_params.LinearSVCParams,
            specs.AvailableModelTypes.SVC: cl_params.SVCParams,
            specs.AvailableModelTypes.LOGISTIC_REGRESSION: cl_params.LogisticRegressionParams,
            specs.AvailableModelTypes.PASSIVE_AGGRESSIVE_CLASSIFIER: cl_params.PassiveAggressiveClassifierParams,
            specs.AvailableModelTypes.K_NEIGHBORS_CLASSIFIER: cl_params.KNeighborsClassifierParams,
            specs.AvailableModelTypes.RADIUS_NEIGHBORS_CLASSIFIER: cl_params.RadiusNeighborsClassifierParams,
            specs.AvailableModelTypes.MLP_CLASSIFIER: cl_params.MLPClassifierParams,
        }
        self._regression_models_params_map = {
            specs.AvailableModelTypes.DECISION_TREE_REGRESSOR: DecisionTreeRegressorParams,
            specs.AvailableModelTypes.RANDOM_FOREST_REGRESSOR: RandomForestRegressorParams,
            specs.AvailableModelTypes.EXTRA_TREES_REGRESSOR: ExtraTreesRegressorParams,
            specs.AvailableModelTypes.GRADIENT_BOOSTING_REGRESSOR: GradientBoostingRegressorParams,
            specs.AvailableModelTypes.ADABOOST_REGRESSOR: AdaBoostRegressorParams,
            specs.AvailableModelTypes.BAGGING_REGRESSOR: BaggingRegressorParams,
            specs.AvailableModelTypes.XGB_REGRESSOR: XGBRegressorParams,
            specs.AvailableModelTypes.LGBM_REGRESSOR: LGBMRegressorParams,
            specs.AvailableModelTypes.CAT_BOOST_REGRESSOR: CatBoostRegressorParams,
            specs.AvailableModelTypes.SGD_REGRESSOR: SGDRegressorParams,
            specs.AvailableModelTypes.LINEAR_SVR: LinearSVRParams,
            specs.AvailableModelTypes.SVR: SVRParams,
            specs.AvailableModelTypes.LINEAR_REGRESSION: LinearRegressionParams,
            specs.AvailableModelTypes.RIDGE: RidgeParams,
            specs.AvailableModelTypes.LASSO: LassoParams,
            specs.AvailableModelTypes.ELASTIC_NET: ElasticNetParams,
            specs.AvailableModelTypes.PASSIVE_AGGRESSIVE_REGRESSOR: PassiveAggressiveRegressorParams,
            specs.AvailableModelTypes.K_NEIGHBORS_REGRESSOR: KNeighborsRegressorParams,
            specs.AvailableModelTypes.RADIUS_NEIGHBORS_REGRESSOR: RadiusNeighborsRegressorParams,
            specs.AvailableModelTypes.MLP_REGRESSOR: MLPRegressorParams,
        }

        self._clustering_models_params_map = {
            specs.AvailableModelTypes.K_MEANS: KMeansParams,
            specs.AvailableModelTypes.MINI_BATCH_KMEANS: MiniBatchKMeansParams,
            specs.AvailableModelTypes.AFFINITY_PROPAGATION: AffinityPropagationParams,
            specs.AvailableModelTypes.MEAN_SHIFT: MeanShiftParams,
            specs.AvailableModelTypes.SPECTRAL_CLUSTERING: SpectralClusteringParams,
            specs.AvailableModelTypes.WARD: WardParams,
            specs.AvailableModelTypes.AGGLOMERATIVE_CLUSTERING: AgglomerativeClusteringParams,
            specs.AvailableModelTypes.DBSCAN: DBSCANParams,
            specs.AvailableModelTypes.OPTICS: OPTICSParams,
            specs.AvailableModelTypes.BIRCH: BirchParams,
            specs.AvailableModelTypes.GAUSSIAN_MIXTURE: GaussianMixtureParams
        }

        self._outlier_detection_models_params_map = {
            specs.AvailableModelTypes.ONE_CLASS_SVM: OneClassSVMParams,
            specs.AvailableModelTypes.SGD_ONE_CLASS_SVM: SGDOneClassSVMParams,
            specs.AvailableModelTypes.ELLIPTIC_ENVELOPE: EllipticEnvelopeParams,
            specs.AvailableModelTypes.LOCAL_OUTLIER_FACTOR: LocalOutlierFactorParams,
            specs.AvailableModelTypes.ISOLATION_FOREST: IsolationForestParams
        }

        self._dimensionality_reduction_models_params_map = {
            specs.AvailableModelTypes.PCA: PCAParams,
            specs.AvailableModelTypes.LINEAR_DISCRIMINANT_ANALYSIS: LinearDiscriminantAnalysisParams,
            specs.AvailableModelTypes.T_SNE: TSNEParams,
            specs.AvailableModelTypes.ISOMAP: IsomapParams,
            specs.AvailableModelTypes.NMF: NMFParams,
            specs.AvailableModelTypes.TRUNCATED_SVD: TruncatedSVDParams
        }

    async def validate_params(self, task_type: specs.AvailableTaskTypes,
                        model_params: schemas.ModelParams,
                        params_type: specs.AvailableParamsTypes,
                        dataframe_id: PydanticObjectId) -> schemas.ModelParams:
        if params_type == specs.AvailableParamsTypes.DEFAULT:
            params = {}
        elif params_type == specs.AvailableParamsTypes.CUSTOM:
            try:
                params = await self._validate_model_params(task_type, model_params)
            except ValidationError as err:
                raise errors.ModelParamsValidationError(model_params, err)
        elif params_type == specs.AvailableParamsTypes.AUTO:
            model_params = await HyperortService(dataframe_id).search_params(model_params.model_type)
            try:
                params = await self._validate_model_params(task_type, model_params)
            except ValidationError as err:
                raise errors.HyperoptModelParamsValidationError(model_params, err)
        else:
            raise errors.UnknownParamsTypeError(params_type)
        return schemas.ModelParams(type=model_params.model_type,
                                   params=params)

    async def _validate_model_params(self, task_type, model_params) -> Dict[str, Any]:
        if task_type == specs.AvailableTaskTypes.CLASSIFICATION:
            params = await self.validate_classification_model_params(model_params)
        elif task_type == specs.AvailableTaskTypes.REGRESSION:
            params = await self.validate_regression_model_params(model_params)
        elif task_type == specs.AvailableTaskTypes.CLUSTERING:
            params = await self.validate_clustering_model_params(model_params)
        elif task_type == specs.AvailableTaskTypes.OUTLIER_DETECTION:
            params = await self.validate_outlier_detection_model_params(model_params)
        elif task_type == specs.AvailableTaskTypes.DIMENSIONALITY_REDUCTION:
            params = await self.validate_dimensionality_reduction_model_params(model_params)
        else:
            raise errors.UnknownTaskTypeError(task_type)
        return params

    async def validate_classification_model_params(self, model_params) -> Dict[str, Any]:
        classification_model = model_params.model_type
        if classification_model not in self._classification_models_params_map:
            raise errors.UnknownClassificationModelError(classification_model)

        model_params_class = self._classification_models_params_map[classification_model]
        validated_params = model_params_class(**model_params.params)
        return validated_params.dict()

    async def validate_regression_model_params(self, model_params) -> Dict[str, Any]:
        regression_model = model_params.model_type
        if regression_model not in self._regression_models_params_map:
            raise errors.UnknownRegressionModelError(regression_model)

        model_params_class = self._regression_models_params_map[regression_model]
        validated_params = model_params_class(**model_params.params)
        return validated_params.dict()

    async def validate_clustering_model_params(self, model_params) -> Dict[str, Any]:
        clustering_model = model_params.model_type
        if clustering_model not in self._clustering_models_params_map:
            raise errors.UnknownClusteringModelError(clustering_model)

        model_params_class = self._clustering_models_params_map[clustering_model]
        validated_params = model_params_class(**model_params.params)
        return validated_params.dict()

    async def validate_outlier_detection_model_params(self, model_params) -> Dict[str, Any]:
        outlier_detection_model = model_params.model_type
        if outlier_detection_model not in self._outlier_detection_models_params_map:
            raise errors.UnknownOutlierDetectionModelError(outlier_detection_model)

        model_params_class = self._outlier_detection_models_params_map[outlier_detection_model]
        validated_params = model_params_class(**model_params.params)
        return validated_params.dict()

    async def validate_dimensionality_reduction_model_params(self, model_params) -> Dict[str, Any]:
        dimensionality_reduction_model = model_params.model_type
        if dimensionality_reduction_model not in self._dimensionality_reduction_models_params_map:
            raise errors.UnknownDimensionalityReductionModelError(dimensionality_reduction_model)

        model_params_class = self._dimensionality_reduction_models_params_map[dimensionality_reduction_model]
        validated_params = model_params_class(**model_params.params)
        return validated_params.dict()

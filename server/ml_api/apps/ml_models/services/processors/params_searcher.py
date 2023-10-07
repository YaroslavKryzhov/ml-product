import traceback

from hyperopt import fmin, tpe, STATUS_OK, space_eval
from sklearn.model_selection import cross_val_score
from sklearn.metrics import silhouette_score
from beanie.odm.fields import PydanticObjectId


from ml_api.apps.ml_models import schemas, errors
from ml_api.apps.ml_models.specs import AvailableTaskTypes as TaskTypes
from ml_api.apps.ml_models.specs import AvailableModelTypes as ModelTypes
from ml_api.apps.dataframes.services.for_model_service import \
    DataframeForModelService
from ml_api.apps.ml_models.services.processors.model_construstor import \
    ModelConstructorService
from ml_api.apps.ml_models.models_specs.hyperopt_params.\
    classification_searchers import CLASSIFICATION_SEARCH_SPACE_CONFIG
from ml_api.apps.ml_models.models_specs.hyperopt_params.regression_searchers \
    import REGRESSION_SEARCH_SPACE_CONFIG
from ml_api.apps.ml_models.models_specs.hyperopt_params.clustering_searchers \
    import CLUSTERING_SEARCH_SPACE_CONFIG


class HyperoptService:
    def __init__(self, user_id, dataframe_id: PydanticObjectId):
        self.target = None
        self.features = None
        self.dataframe_id = dataframe_id
        self.user_id = user_id

        self._task_to_searcher_params_map = {
            TaskTypes.CLASSIFICATION: CLASSIFICATION_SEARCH_SPACE_CONFIG,
            TaskTypes.REGRESSION: REGRESSION_SEARCH_SPACE_CONFIG,
            TaskTypes.CLUSTERING: CLUSTERING_SEARCH_SPACE_CONFIG,
        }

        self._task_to_model_error_map = {
            TaskTypes.CLASSIFICATION: errors.UnknownClassificationModelError,
            TaskTypes.REGRESSION: errors.UnknownRegressionModelError,
            TaskTypes.CLUSTERING: errors.UnknownClusteringModelError,
        }

    async def search_params(self, task_type: TaskTypes,
                            model_type: ModelTypes) -> schemas.ModelParams:
        await self._prepare_data(task_type)

        search_space = self.get_model_params_search_space(task_type, model_type)

        best = fmin(fn=lambda params: self._objective(params, task_type, model_type),
                    space=search_space,
                    algo=tpe.suggest,
                    max_evals=50)
        try:
            best_params = space_eval(search_space, best)
        except Exception as err:
            print(traceback.format_exc())
            error_type = type(err).__name__
            error_description = str(err)
            raise errors.ParamsSearchingError(
                model_type.value, f"{error_type}: {error_description}")

        return schemas.ModelParams(model_type=model_type, params=best_params)

    async def _prepare_data(self, task_type: TaskTypes):
        # TODO: move data loading out of hyperopt service
        if task_type in [TaskTypes.CLASSIFICATION,
                         TaskTypes.REGRESSION]:
            self.features, self.target = await DataframeForModelService(
                self.user_id).get_feature_target_df_supervised(self.dataframe_id)
        elif task_type == TaskTypes.CLUSTERING:
            self.features, _ = await DataframeForModelService(
                self.user_id).get_feature_target_df(self.dataframe_id)
        elif task_type in [TaskTypes.OUTLIER_DETECTION,
                         TaskTypes.DIMENSIONALITY_REDUCTION]:
            raise errors.HyperoptTaskTypeError(task_type)
        else:
            raise errors.UnknownTaskTypeError(task_type.value)

    def get_model_params_search_space(self, task_type: TaskTypes,
                                      model_type: ModelTypes):
        if task_type not in self._task_to_searcher_params_map:
            raise errors.UnknownTaskTypeError(task_type.value)
        searcher_params_map = self._task_to_searcher_params_map[task_type]

        if model_type not in searcher_params_map:
            unknown_model_err = self._task_to_model_error_map[task_type]
            raise unknown_model_err(model_type)
        return searcher_params_map[model_type]

    def _objective(self, params, task_type, model_type):
        model_params = schemas.ModelParams(model_type=model_type, params=params)
        model = ModelConstructorService().get_model(task_type, model_params)

        if task_type == TaskTypes.CLASSIFICATION:
            scoring_method = 'roc_auc_weighted' if \
                len(self.target.unique()) > 2 else 'roc_auc'
            scores = cross_val_score(model, self.features, self.target,
                scoring=scoring_method, cv=5, n_jobs=-1, error_score="raise")
            loss = -scores.mean()

        elif task_type == TaskTypes.REGRESSION:
            scores = cross_val_score(model, self.features, self.target,
                scoring='mse', cv=5, n_jobs=-1, error_score="raise")
            loss = -scores.mean()

        elif task_type == TaskTypes.CLUSTERING:
            model.fit(self.features)
            labels = model.labels_
            loss = -silhouette_score(self.features, labels)
        else:
            raise errors.UnknownTaskTypeError(task_type.values_to_fill)

        return {'loss': loss, 'status': STATUS_OK}

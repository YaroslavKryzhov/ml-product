from hyperopt import fmin, tpe, hp, STATUS_OK, space_eval
from sklearn.model_selection import cross_val_score
from sklearn.metrics import silhouette_score

from ml_api.apps.dataframes.services.dataframe_manager import \
    DataframeManagerService
from ml_api.apps.ml_models import schemas, specs, errors
from ml_api.apps.ml_models.services.model_construstor import \
    ModelConstructorService
from ml_api.apps.ml_models.specs import AvailableTaskTypes as task_types


class HyperoptService:
    def __init__(self, dataframe_info: schemas.DataframeGetterInfo):
        self.target = None
        self.features = None
        self.dataframe_id = dataframe_info.dataframe_id
        self.user_id = dataframe_info.user_id

    async def _prepare_data(self, task_type):
        if task_type in [task_types.CLASSIFICATION,
                         task_types.REGRESSION]:
            self.features, self.target = DataframeManagerService(
                self.user_id).get_feature_target_df(self.dataframe_id)

        if task_type == task_types.CLUSTERING:
            self.features = DataframeManagerService(
                self.user_id).get_feature_df(self.dataframe_id)

        if task_type in [task_types.OUTLIER_DETECTION,
                         task_types.DIMENSIONALITY_REDUCTION]:
            raise errors.HyperoptTaskTypeError(task_type)

        else:
            raise errors.UnknownTaskTypeError(task_type)

    def get_model_params_search_space(self, model_type):
        # TODO: write map for params searcher
        # Здесь можно определить пространство поиска для каждого типа модели
        # Возвращаем словарь с параметрами
        # classification_searchers.CLASSIFICATION_CONFIG.get(
        #     model_type.value, None
        # )
        return {
            # Пример для DecisionTreeClassifier
            specs.AvailableModelTypes.DECISION_TREE_CLASSIFIER: {
                'criterion': hp.choice('criterion', ['gini', 'entropy']),
                'splitter': hp.choice('splitter', ['best', 'random']),
                'max_depth': hp.quniform('max_depth', 1, 20, 1)
            },
            # Добавьте другие модели с их параметрами
        }.get(model_type, {})

    async def search_params(self, task_type: task_types,
                            model_type: specs.AvailableModelTypes) -> schemas.ModelParams:
        await self._prepare_data(task_type)

        search_space = self.get_model_params_search_space(model_type)

        best = fmin(fn=lambda params: self._objective(params, task_type, model_type),
                    space=search_space,
                    algo=tpe.suggest,
                    max_evals=50)
        best_params = space_eval(search_space, best)

        return schemas.ModelParams(model_type=model_type, params=best_params)

    def _objective(self, params, task_type, model_type):
        model_params = schemas.ModelParams(model_type=model_type, params=params)
        model = await ModelConstructorService().get_model(task_type, model_params)
        del model_params

        if task_type == task_types.CLASSIFICATION:
            scoring_method = 'roc_auc_ovr' if len(self.target.unique()) > 2 \
                else 'roc_auc'
            scores = cross_val_score(model, self.features, self.target,
                                     scoring=scoring_method,
                                     cv=5,
                                     n_jobs=-1,
                                     error_score="raise")
            loss = -scores.mean()

        elif task_type == task_types.REGRESSION:
            scores = cross_val_score(model, self.features, self.target,
                scoring='mse',
                cv=5,
                n_jobs=-1,
                error_score="raise",
            )
            loss = -scores.mean()

        elif task_type == task_types.CLUSTERING:
            model.fit(self.features)
            labels = model.labels_
            loss = -silhouette_score(self.features, labels)

        else:
            raise errors.UnknownTaskTypeError(task_type)

        return {'loss': loss, 'status': STATUS_OK}

from typing import List, Dict, Any
from functools import partial

from hyperopt import fmin, tpe, STATUS_OK, space_eval
from sklearn.model_selection import StratifiedKFold, cross_val_score

from ml_api.apps.ml_models.utils import classification_searchers, \
    regression_searchers
from ml_api.apps.ml_models.schemas import CompositionParams
from ml_api.apps.ml_models.specs import AvailableModelTypes, AvailableTaskTypes
from ml_api.apps.ml_models.services.model_construstor import ModelConstructor


class SearchParamsException(Exception):
    pass


class AutoParamsSearch:
    def __init__(
            self,
            task_type: AvailableTaskTypes,
            composition_params: List[CompositionParams],
            features,
            target,
    ):
        self.task_type = task_type
        self.composition_params = composition_params
        self.features = features
        self.target = target

    def search_params(self):
        for i, model_data in enumerate(self.composition_params):
            self.composition_params[i].params = self._validate_params(
                model_data.type
            )
        return self.composition_params

    def _validate_params(self, model_type: AvailableModelTypes
                         ) -> Dict[str, Any]:
        if self.task_type == AvailableTaskTypes.CLASSIFICATION:
            search_space = classification_searchers.CLASSIFICATION_CONFIG.get(
                model_type.value, None
            )
            if search_space is None:
                raise SearchParamsException(
                    f'Unavailable model: Model {model_type.value} not '
                    f'found in searchers config')
            if self.target.nunique() == 2:
                best = fmin(
                    fn=partial(self._objective_binary, model_type=model_type),
                    space=search_space,
                    algo=tpe.suggest,
                    max_evals=50,
                    show_progressbar=True,
                )
                return space_eval(search_space, best)
            else:
                best = fmin(
                    fn=partial(
                        self._objective_multiclass, model_type=model_type
                    ),
                    space=search_space,
                    algo=tpe.suggest,
                    max_evals=50,
                    show_progressbar=True,
                )
                return space_eval(search_space, best)
        elif self.task_type == AvailableTaskTypes.REGRESSION:
            search_space = regression_searchers.REGRESSION_CONFIG.get(
                model_type.value, None
            )
            # TODO: fill regression config at utils/regression_searchers
            if search_space is None:
                raise SearchParamsException(
                    f'Unavailable model: Model {model_type.value} not '
                    f'found in searchers config')
            best = fmin(
                fn=partial(self._objective_regression, model_type=model_type),
                space=search_space,
                algo=tpe.suggest,
                max_evals=50,
                show_progressbar=True,
            )
            return space_eval(search_space, best)
        else:
            raise SearchParamsException(
                f'Unknown task type: {self.task_type}')

    def _objective_binary(self, params, model_type: AvailableModelTypes):
        model = ModelConstructor(
            task_type=self.task_type, model_type=model_type, params=params
        ).get_model()
        skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=1)
        score = cross_val_score(
            estimator=model,
            X=self.features,
            y=self.target,
            scoring='roc_auc',
            cv=skf,
            n_jobs=-1,
            error_score="raise",
        )
        return {'loss': -score.mean(), 'params': params, 'status': STATUS_OK}

    def _objective_multiclass(self, params, model_type: AvailableModelTypes):
        model = ModelConstructor(
            task_type=self.task_type, model_type=model_type, params=params
        ).get_model()
        skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=1)
        score = cross_val_score(
            estimator=model,
            X=self.features,
            y=self.target,
            scoring='roc_auc_ovr_weighted',
            cv=skf,
            n_jobs=-1,
            error_score="raise",
        )
        return {'loss': -score.mean(), 'params': params, 'status': STATUS_OK}

    def _objective_regression(self, params, model_type: AvailableModelTypes):
        model = ModelConstructor(
            task_type=self.task_type, model_type=model_type, params=params
        ).get_model()
        skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=1)
        score = cross_val_score(
            estimator=model,
            X=self.features,
            y=self.target,
            scoring='mse',
            cv=skf,
            n_jobs=-1,
            error_score="raise",
        )
        return {'loss': -score.mean(), 'params': params, 'status': STATUS_OK}

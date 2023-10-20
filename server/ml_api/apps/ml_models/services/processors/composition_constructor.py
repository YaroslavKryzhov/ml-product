import traceback
from typing import Dict, Any

from sklearn import ensemble, linear_model

from ml_api.apps.ml_models import schemas, errors
from ml_api.apps.ml_models.models import ModelMetadata
from ml_api.apps.ml_models.specs import AvailableModelTypes as Models
from ml_api.apps.ml_models.specs import AvailableTaskTypes as TaskTypes


class CompositionConstructorService:
    def __init__(self):

        self._classification_composition_map = {
            Models.VOTING_CLASSIFIER: self._get_voting_classifier,
            Models.STACKING_CLASSIFIER: self._get_stacking_classifier,
        }

        self._regression_composition_map = {
            Models.VOTING_REGRESSOR: self._get_voting_regressor,
            Models.STACKING_REGRESSOR: self._get_stacking_regressor,
        }

        self._task_to_composition_map_map = {
            TaskTypes.CLASSIFICATION: self._classification_composition_map,
            TaskTypes.REGRESSION: self._regression_composition_map,
        }

        self._task_to_composition_error_map = {
            TaskTypes.CLASSIFICATION: errors.UnknownClassificationCompositionError,
            TaskTypes.REGRESSION: errors.UnknownRegressionCompositionError,
        }

    async def get_composition(self, composition_meta: ModelMetadata,
                        composition_params: schemas.ModelParams, estimators):
        composition_type = composition_params.model_type
        task_type = composition_meta.task_type

        if task_type not in self._task_to_composition_map_map:
            raise errors.UnknownTaskTypeError(task_type.value)
        composition_map = self._task_to_composition_map_map[task_type]

        if composition_type not in composition_map:
            unknown_composition_err = self._task_to_composition_error_map[task_type]
            raise unknown_composition_err(composition_type)

        try:
            composition = composition_map[composition_type](
                composition_params.params, estimators)
        except Exception as err:
            print(traceback.format_exc())
            error_type = type(err).__name__
            error_description = str(err)
            raise errors.CompositionConstructionError(f"{error_type}: {error_description}")
        return composition

    def _get_voting_classifier(self, composition_params: Dict[str, Any], models):
        if composition_params['voting'] == 'hard':
            return ensemble.VotingClassifier(estimators=models, voting='hard')
        elif composition_params['voting'] == 'soft':
            return ensemble.VotingClassifier(estimators=models, voting='soft')

    def _get_voting_regressor(self, composition_params: Dict[str, Any], models):
        if composition_params['voting'] == 'hard':
            return ensemble.VotingRegressor(estimators=models, voting='hard')
        elif composition_params['voting'] == 'soft':
            return ensemble.VotingRegressor(estimators=models, voting='soft')

    def _get_stacking_classifier(self, composition_params: Dict[str, Any], estimators):
        final_estimator = self._get_final_classification_estimator(
            composition_params['final_estimator'])
        return ensemble.StackingClassifier(
            estimators=estimators,
            final_estimator=final_estimator)

    def _get_stacking_regressor(self, composition_params: Dict[str, Any], estimators):
        final_estimator = self._get_final_regression_estimator(
            composition_params['final_estimator'])
        return ensemble.StackingRegressor(
            estimators=estimators,
            final_estimator=final_estimator)

    def _get_final_classification_estimator(self, final_estimator: str):
        if final_estimator == 'LogisticRegression':
            return linear_model.LogisticRegression()
        elif final_estimator == 'RandomForestClassifier':
            return ensemble.RandomForestClassifier()
        elif final_estimator == 'GradientBoostingClassifier':
            return ensemble.GradientBoostingClassifier()

    def _get_final_regression_estimator(self, final_estimator: str):
        if final_estimator == 'RidgeCV':
            return linear_model.RidgeCV()
        elif final_estimator == 'RandomForestRegressor':
            return ensemble.RandomForestRegressor()
        elif final_estimator == 'GradientBoostingRegressor':
            return ensemble.GradientBoostingRegressor()

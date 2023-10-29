from pydantic import ValidationError

from ml_api.apps.ml_models import schemas, errors
from ml_api.apps.ml_models.model import ModelMetadata
from ml_api.apps.ml_models.specs import AvailableModelTypes as Models
from ml_api.apps.ml_models.specs import AvailableTaskTypes as TaskTypes
from ml_api.apps.ml_models.models_specs.validation_params import \
    classification_compositions_params as classif_params, \
    regression_compositions_params as regr_params


class CompositionParamsValidator:
    def __init__(self, composition_meta: ModelMetadata):
        self.composition_meta = composition_meta
        self.task_type = composition_meta.task_type
        self.composition_type = composition_meta.model_params.model_type
        self.composition_params = composition_meta.model_params.params

        self._classification_compositions_params_map = {
            Models.VOTING_CLASSIFIER: classif_params.VotingClassifierParams,
            Models.STACKING_CLASSIFIER: classif_params.StackingClassifierParams,
        }

        self._regression_compositions_params_map = {
            Models.VOTING_REGRESSOR: regr_params.VotingRegressorParams,
            Models.STACKING_REGRESSOR: regr_params.StackingRegressorParams,
        }

        self._task_to_compositions_params_map_map = {
            TaskTypes.CLASSIFICATION: self._classification_compositions_params_map,
            TaskTypes.REGRESSION: self._regression_compositions_params_map,
        }

        self._task_to_composition_error_map = {
            TaskTypes.CLASSIFICATION: errors.UnknownClassificationCompositionError,
            TaskTypes.REGRESSION: errors.UnknownRegressionCompositionError,
        }

    async def validate_params(self) -> schemas.ModelParams:
        if self.task_type not in self._task_to_compositions_params_map_map:
            raise errors.UnknownTaskTypeError(self.task_type.value)
        compositions_params_map = self._task_to_compositions_params_map_map[self.task_type]

        if self.composition_type not in compositions_params_map:
            unknown_composition_err = self._task_to_composition_error_map[self.task_type]
            raise unknown_composition_err(self.composition_type)
        compositions_params_class = compositions_params_map[self.composition_type]

        try:
            validated_params = compositions_params_class(**self.composition_params)
        except ValidationError as err:
            raise errors.ModelParamsValidationError(
                self.composition_type.value, self.composition_params, str(err))
        return schemas.ModelParams(
            model_type=self.composition_type,
            params=validated_params.dict()
        )

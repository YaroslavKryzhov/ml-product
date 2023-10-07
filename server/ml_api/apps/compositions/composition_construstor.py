from typing import List

from sklearn import ensemble
from ml_api.apps.ml_models import schemas, specs
from ml_api.apps.ml_models.services.processors.model_construstor import ModelConstructor


class ConstructCompositionException(Exception):
    pass


class CompositionConstructor:
    """
    Creates sklearn composition/model with fit(), predict() methods
    Uses ModelConstructor class for component estimators
    """

    def __init__(
            self,
            task_type: specs.AvailableTaskTypes,
            composition_type: specs.AvailableCompositionTypes,
            composition_params: List[schemas.CompositionParams],
    ):
        """
        :param task_type: one of ml_models.schemas.AvailableTaskTypes
        :param composition_type: one of ml_models.schemas.AvailableCompositions
        :param composition_params: list of ml_models.schemas.CompositionParams
        """
        self.task_type = task_type
        self.composition_type = composition_type
        self.composition_params = composition_params

    def build_composition(self):
        if self.task_type == specs.AvailableTaskTypes.CLASSIFICATION:
            return self._build_classification_composition()
        elif self.task_type == specs.AvailableTaskTypes.REGRESSION:
            return self._build_regression_composition()
        else:
            raise ConstructCompositionException(
                f'Unknown task type: {self.task_type}')

    def _build_classification_composition(self):
        """
        Creates composition for CompositionValidator class.
        If composition_type is 'none' returns sklearn model;
        If 'simple_voting' - VotingClassifier without weights;
        If 'weighted_voting' - VotingClassifier with weights;
        If 'stacking' - StackingClassifier with GradientBoosting on head;
        :return:
        sklearn estimator
        """
        models = []
        if self.composition_type == specs.AvailableCompositionTypes.NONE:
            model = self.composition_params[0]
            composition = ModelConstructor(
                task_type=self.task_type,
                model_type=model.model_type,
                params=model.params,
            ).get_model()
            return composition
        for i, model in enumerate(self.composition_params):
            models.append(
                (
                    str(i) + "_" + model.model_type.values_to_fill,
                    ModelConstructor(
                        task_type=self.task_type,
                        model_type=model.model_type,
                        params=model.params,
                    ).get_model(),
                )
            )
        if self.composition_type == specs.AvailableCompositionTypes.SIMPLE_VOTING:
            composition = ensemble.VotingClassifier(estimators=models,
                                                    voting='hard')
            return composition
        elif self.composition_type == specs.AvailableCompositionTypes.WEIGHTED_VOTING:
            composition = ensemble.VotingClassifier(estimators=models,
                                                    voting='soft')
            return composition
        elif self.composition_type == specs.AvailableCompositionTypes.STACKING:
            final_estimator = ensemble.GradientBoostingClassifier()
            composition = ensemble.StackingClassifier(
                estimators=models,
                final_estimator=final_estimator)
            return composition
        else:
            raise ConstructCompositionException(
                f'Unknown composition type: {self.composition_type}')

    def _build_regression_composition(self):
        raise NotImplementedError

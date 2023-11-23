import traceback

import pandas as pd
from sklearn.model_selection import train_test_split

from ml_api.apps.ml_models import errors, utils, specs
from ml_api.apps.ml_models.specs import AvailableTaskTypes as TaskTypes
from ml_api.apps.ml_models.model import ModelMetadata
from ml_api.apps.ml_models.schemas import ModelTrainingResults
from ml_api.apps.training_reports.services import ReportCreatorService


class CompositionValidationService:
    def __init__(self, composition_meta: ModelMetadata, composition):
        self.composition = composition
        self.task_type = composition_meta.task_type
        self.composition_type = composition_meta.model_params.model_type
        self.model_id = composition_meta.id
        self.dataframe_id = composition_meta.dataframe_id
        self.feature_columns = composition_meta.feature_columns
        self.target_column = composition_meta.target_column
        self.stratify = composition_meta.stratify
        self.test_size = composition_meta.test_size

        self.report_creator = ReportCreatorService()
        self.classes_limit = 10
        self._task_to_method_map = {
            TaskTypes.CLASSIFICATION: self._process_classification,
            TaskTypes.REGRESSION: self._process_regression,
        }

    def _get_train_test_split(self, features, target):
        stratify = target if self.stratify else None
        return train_test_split(features, target, test_size=self.test_size,
                                stratify=stratify)

    def _get_probabilities(self, f_valid):
        try:
            probabilities = self.composition.predict_proba(f_valid)
            if probabilities.shape[1] == 2:  # Бинарная классификация
                return probabilities[:, 1]
            else:  # Многоклассовая классификация
                return probabilities
        except AttributeError:
            try:
                return self.composition.decision_function(f_valid)
            except AttributeError:
                return None

    def validate_composition(self, composition_meta, features, target) -> ModelTrainingResults:
        if self.task_type not in self._task_to_method_map.keys():
            raise errors.UnknownTaskTypeError(self.task_type.value)
        process_validation = self._task_to_method_map[self.task_type]
        try:
            composition_validation_result = process_validation(features, target)
        except Exception as err:
            # print(traceback.format_exc())
            error_type = type(err).__name__
            error_description = str(err)
            raise errors.CompositionValidationError(f"{error_type}: {error_description}")
        return composition_validation_result

    def _process_classification(self, features, target) -> ModelTrainingResults:
        num_classes = target.nunique()
        if num_classes < 2:
            raise errors.OneClassClassificationError(self.dataframe_id)
        elif num_classes > self.classes_limit:
            raise errors.TooManyClassesClassificationError(
                num_classes, self.dataframe_id)

        # can be joined with ModelTrainer

        f_train, f_valid, t_train, t_valid = self._get_train_test_split(
                features, target)
        self.composition.fit(f_train, t_train)

        preds = pd.Series(self.composition.predict(f_valid),
                          name=self.target_column)
        probs = self._get_probabilities(f_valid)
        results_df = utils.get_predictions_df(f_valid, preds)
        if num_classes == 2:
            report = self.report_creator.score_binary_classification(
                t_valid, preds, probs)
        else:
            classes = list(target.unique())
            report = self.report_creator.score_multiclass_classification(
                classes, t_valid, preds, probs)
        return ModelTrainingResults(
            model=self.composition,
            results=[(report, results_df)],
        )

    def _process_regression(self, features, target) -> ModelTrainingResults:
        if self.composition_type == specs.AvailableModelTypes.STACKING_REGRESSOR:
            f_train, f_valid, t_train, t_valid = self._get_train_test_split(
                features, target)
            self.composition.fit(f_train, t_train)
        elif self.composition_type == specs.AvailableModelTypes.VOTING_REGRESSOR:
            f_valid, t_valid = features, target
        else:
            raise errors.UnknownCompositionTypeError(self.composition_type.value)

        preds = pd.Series(self.composition.predict(f_valid),
                          name=self.target_column)
        results_df = utils.get_predictions_df(f_valid, preds)
        report = self.report_creator.score_regression(t_valid, preds)
        return ModelTrainingResults(
            model=self.composition,
            results=[(report, results_df)],
        )

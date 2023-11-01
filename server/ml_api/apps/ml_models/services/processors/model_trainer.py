import traceback

import pandas as pd
from sklearn.model_selection import train_test_split

from ml_api.apps.ml_models import errors, utils
from ml_api.apps.ml_models.specs import AvailableTaskTypes as TaskTypes
from ml_api.apps.ml_models.model import ModelMetadata
from ml_api.apps.ml_models.schemas import ModelTrainingResults
from ml_api.apps.training_reports.services.report_creator import ReportCreatorService


class ModelTrainerService:
    def __init__(self, model_meta: ModelMetadata, model):
        self.model = model
        self.task_type = model_meta.task_type
        self.model_id = model_meta.id
        self.dataframe_id = model_meta.dataframe_id
        self.feature_columns = model_meta.feature_columns
        self.target_column = model_meta.target_column
        self.test_size = model_meta.test_size
        self.stratify = model_meta.stratify

        self.report_creator = ReportCreatorService()
        self.classes_limit = 10
        self._task_to_method_map = {
            TaskTypes.CLASSIFICATION: self._process_classification,
            TaskTypes.REGRESSION: self._process_regression,
            TaskTypes.CLUSTERING: self._process_clustering,
            TaskTypes.OUTLIER_DETECTION: self._process_outlier_detection,
            TaskTypes.DIMENSIONALITY_REDUCTION: self._process_dimensionality_reduction,
        }

    def _get_train_test_split(self, features, target):
        stratify = target if self.stratify else None
        return train_test_split(features, target, test_size=self.test_size,
                                stratify=stratify)

    def _fit_and_predict(self, f_train, t_train, f_valid):
        self.model.fit(f_train, t_train)
        return pd.Series(self.model.predict(f_train), name=self.target_column), \
               pd.Series(self.model.predict(f_valid), name=self.target_column)

    def _get_probabilities(self, f_valid):
        try:
            probabilities = self.model.predict_proba(f_valid)
            if probabilities.shape[1] == 2:  # Бинарная классификация
                return probabilities[:, 1]
            else:  # Многоклассовая классификация
                return probabilities
        except AttributeError:
            try:
                return self.model.decision_function(f_valid)
            except AttributeError:
                return None

    async def train_model(self, model_meta, features, target) -> ModelTrainingResults:
        if self.task_type not in self._task_to_method_map.keys():
            raise errors.UnknownTaskTypeError(self.task_type.value)
        process_train = self._task_to_method_map[self.task_type]
        try:
            model_training_result = await process_train(features, target)
        except Exception as err:
            print(traceback.format_exc())
            error_type = type(err).__name__
            error_description = str(err)
            raise errors.ModelTrainingError(f"{error_type}: {error_description}")
        return model_training_result

    async def _process_classification(self, features, target) -> ModelTrainingResults:
        num_classes = target.nunique()
        if num_classes < 2:
            raise errors.OneClassClassificationError(self.dataframe_id)
        elif num_classes > self.classes_limit:
            raise errors.TooManyClassesClassificationError(
                num_classes, self.dataframe_id)

        f_train, f_valid, t_train, t_valid = self._get_train_test_split(
            features, target)

        train_preds, valid_preds = self._fit_and_predict(f_train, t_train, f_valid)
        train_probs = self._get_probabilities(f_train)
        valid_probs = self._get_probabilities(f_valid)

        train_results_df = utils.get_predictions_df(f_train, train_preds)
        valid_results_df = utils.get_predictions_df(f_valid, valid_preds)

        if num_classes == 2:
            train_report = self.report_creator.score_binary_classification(
                t_train, train_preds, train_probs, is_train=True)
            valid_report = self.report_creator.score_binary_classification(
                t_valid, valid_preds, valid_probs)
        else:
            classes = list(target.unique())
            train_report = self.report_creator.score_multiclass_classification(
                classes, t_train, train_preds, train_probs, is_train=True)
            valid_report = self.report_creator.score_multiclass_classification(
                classes, t_valid, valid_preds, valid_probs)
        return ModelTrainingResults(
            model=self.model,
            results=[(train_report, train_results_df),
                     (valid_report, valid_results_df)],
        )

    async def _process_regression(self, features, target) -> ModelTrainingResults:
        f_train, f_valid, t_train, t_valid = self._get_train_test_split(
            features, target)
        train_preds, valid_preds = self._fit_and_predict(f_train, t_train,
                                                         f_valid)

        train_results_df = utils.get_predictions_df(f_train, train_preds)
        valid_results_df = utils.get_predictions_df(f_valid, valid_preds)

        train_report = self.report_creator.score_regression(
            t_train, train_preds, is_train=True)

        valid_report = self.report_creator.score_regression(t_valid, valid_preds)
        return ModelTrainingResults(
            model=self.model,
            results=[(train_report, train_results_df),
                     (valid_report, valid_results_df)],
        )

    async def _process_clustering(self, features, target) -> ModelTrainingResults:
        self.model.fit(features)
        labels = pd.Series(self.model.labels_)

        results_df = utils.get_predictions_df(features, labels)
        report = self.report_creator.score_clustering(features, labels,
                                                      is_train=True)

        return ModelTrainingResults(
            model=self.model,
            results=[(report, results_df)],
        )

    async def _process_outlier_detection(self, features, target) -> ModelTrainingResults:
        outliers = self.model.fit_predict(features)
        outliers = pd.Series(outliers).replace({1: False, -1: True})

        results_df = utils.get_predictions_df(features, outliers)

        report = self.report_creator.score_outlier_detection(
            features, outliers, is_train=True)
        return ModelTrainingResults(
            model=self.model,
            results=[(report, results_df)],
        )

    async def _process_dimensionality_reduction(self, features, target) -> ModelTrainingResults:
        reduced_features = self.model.fit_transform(features)

        if target is not None:
            results_df = utils.get_predictions_df(reduced_features, target)
        else:
            results_df = reduced_features

        report = self.report_creator.score_dimensionality_reduction(
            self.model.explained_variance_ratio_, is_train=True)
        return ModelTrainingResults(
            model=self.model,
            results=[(report, results_df)],
        )

from typing import Optional

import pandas as pd
from sklearn.model_selection import train_test_split

from ml_api.apps.dataframes.services.dataframe_manager import DataframeManagerService
from ml_api.apps.ml_models import errors, utils
from ml_api.apps.ml_models.specs import AvailableTaskTypes as TaskTypes
from ml_api.apps.ml_models.models import ModelMetadata
from ml_api.apps.ml_models.schemas import ModelTrainingResults
from ml_api.apps.training_reports.services.report_creator import ReportCreatorService


class ModelTrainerService:
    def __init__(self, user_id, model_meta: ModelMetadata, model):
        self._user_id = user_id
        self.model = model
        self.task_type = model_meta.task_type
        self.model_id = model_meta.id
        self.dataframe_id = model_meta.dataframe_id
        self.feature_columns = model_meta.feature_columns
        self.target_column = model_meta.target_column
        self.test_size = model_meta.test_size
        self.stratify = model_meta.stratify

        self.dataframe_manager = DataframeManagerService(self._user_id)
        self.report_creator = ReportCreatorService()
        self.classes_limit = 10
        self._task_to_method_map = {
            TaskTypes.CLASSIFICATION: self._process_classification,
            TaskTypes.REGRESSION: self._process_regression,
            TaskTypes.CLUSTERING: self._process_clustering,
            TaskTypes.OUTLIER_DETECTION: self._process_outlier_detection,
            TaskTypes.DIMENSIONALITY_REDUCTION: self._process_dimensionality_reduction,
        }

    async def _get_train_data(self) -> (pd.DataFrame, Optional[pd.Series]):
        if self.task_type in [TaskTypes.CLASSIFICATION, TaskTypes.REGRESSION]:
            return await self.dataframe_manager.\
                get_feature_target_df_supervised(dataframe_id=self.dataframe_id)
        else:
            return await self.dataframe_manager.get_feature_target_df(
                dataframe_id=self.dataframe_id)

    def _get_train_test_split(self, features, target):
        stratify = target if self.stratify else None
        return train_test_split(features, target, test_size=self.test_size,
                                stratify=stratify)

    def _fit_and_predict(self, f_train, t_train, f_valid):
        self.model.fit(f_train, t_train)
        return pd.Series(self.model.predict(f_train)), \
               pd.Series(self.model.predict(f_valid))

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

    async def train_model(self) -> ModelTrainingResults:
        if self.task_type not in self._task_to_method_map:
            raise errors.UnknownTaskTypeError(self.task_type)
        process_train = self._task_to_method_map[self.task_type]
        model_training_result = await process_train()
        return model_training_result

    async def _process_classification(self) -> ModelTrainingResults:
        features, target = await self._get_train_data()
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

        train_results_df = utils.get_predictions_df(features, train_preds)
        valid_results_df = utils.get_predictions_df(features, valid_preds)

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

    async def _process_regression(self) -> ModelTrainingResults:
        features, target = await self._get_train_data()
        f_train, f_valid, t_train, t_valid = self._get_train_test_split(
            features, target)
        train_preds, valid_preds = self._fit_and_predict(f_train, t_train,
                                                         f_valid)

        train_results_df = utils.get_predictions_df(features, train_preds)
        valid_results_df = utils.get_predictions_df(features, valid_preds)

        train_report = self.report_creator.score_regression(
            t_train, train_preds, is_train=True)

        valid_report = self.report_creator.score_regression(t_valid, valid_preds)
        return ModelTrainingResults(
            model=self.model,
            results=[(train_report, train_results_df),
                     (valid_report, valid_results_df)],
        )

    async def _process_clustering(self) -> ModelTrainingResults:
        features, _ = await self._get_train_data()

        self.model.fit(features)
        labels = pd.Series(self.model.labels_)

        results_df = utils.get_predictions_df(features, labels)
        report = self.report_creator.score_clustering(features, labels,
                                                      is_train=True)

        return ModelTrainingResults(
            model=self.model,
            results=[(report, results_df)],
        )

    async def _process_outlier_detection(self) -> ModelTrainingResults:
        features, _ = await self._get_train_data()
        outliers = self.model.fit_predict(features)
        outliers = pd.Series(outliers).replace({1: False, -1: True})

        results_df = utils.get_predictions_df(features, outliers)

        report = self.report_creator.score_outlier_detection(
            features, outliers, is_train=True)
        return ModelTrainingResults(
            model=self.model,
            results=[(report, results_df)],
        )

    async def _process_dimensionality_reduction(self) -> ModelTrainingResults:
        features, target = await self._get_train_data()

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

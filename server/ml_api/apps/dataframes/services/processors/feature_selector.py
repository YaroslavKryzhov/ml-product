import traceback
from typing import List, Dict, Any, Callable, Optional

import numpy as np
from pydantic import ValidationError
from sklearn.feature_selection import VarianceThreshold, SelectKBest
from sklearn.feature_selection import f_classif, f_regression
from sklearn.feature_selection import SelectPercentile, SelectFpr, SelectFdr, \
    SelectFwe, RFE, SequentialFeatureSelector
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import pandas as pd

from ml_api.apps.dataframes import schemas, specs, errors
from ml_api.apps.dataframes.specs import FeatureSelectionMethods as fs


class FeatureSelector:
    """
    Класс, отвечающий за отбор признаков.
    """
    def __init__(self,
                 features: pd.DataFrame,
                 target: pd.Series,
                 task_type: specs.FeatureSelectionTaskType,
                 selector_params: List[schemas.SelectorMethodParams]):
        self.X = features
        self.y = target
        self.task_type = task_type
        self.summary = pd.DataFrame(index=features.columns)
        self.params = selector_params
        self._methods_map = {
            fs.VARIANCE_THRESHOLD: self._variance_threshold,
            fs.SELECT_K_BEST: self._select_k_best,
            fs.SELECT_PERCENTILE: self._select_percentile,
            fs.SELECT_FPR: self._select_fpr,
            fs.SELECT_FDR: self._select_fdr,
            fs.SELECT_FWE: self._select_fwe,
            fs.RECURSIVE_FEATURE_ELIMINATION: self._recursive_feature_elimination,
            fs.SELECT_FROM_MODEL: self._select_from_model,
            fs.SEQUENTIAL_FORWARD_SELECTION: self._sequential_forward_selection,
            fs.SEQUENTIAL_BACKWARD_SELECTION: self._sequential_backward_selection,
        }
        self._params_map = {
            fs.VARIANCE_THRESHOLD: schemas.VarianceThresholdParams,
            fs.SELECT_K_BEST: schemas.SelectKBestParams,
            fs.SELECT_PERCENTILE: schemas.SelectPercentileParams,
            fs.SELECT_FPR: schemas.SelectFprFdrFweParams,
            fs.SELECT_FDR: schemas.SelectFprFdrFweParams,
            fs.SELECT_FWE: schemas.SelectFprFdrFweParams,
            fs.RECURSIVE_FEATURE_ELIMINATION: schemas.RFEParams,
            fs.SELECT_FROM_MODEL: schemas.SelectFromModelParams,
            fs.SEQUENTIAL_FORWARD_SELECTION: schemas.SfsSbsParams,
            fs.SEQUENTIAL_BACKWARD_SELECTION: schemas.SfsSbsParams,
        }

    def get_empty_summary(self) -> schemas.FeatureSelectionSummary:
        for method_param in self.params:
            method_name = method_param.method_name
            if method_name not in self._methods_map:
                raise errors.SelectorMethodNotExistsError(method_name.value)
            self.summary[method_name.value] = None
        result = self.summary.to_dict(orient="index")
        return schemas.FeatureSelectionSummary(result=result)

    def get_summary(self) -> schemas.FeatureSelectionSummary:
        for method_param in self.params:
            method_name = method_param.method_name
            params = method_param.params
            if method_name not in self._methods_map:
                raise errors.SelectorMethodNotExistsError(method_name.value)
            params = self._validate_params(method_name, params)
            try:
                support = self._methods_map[method_name](params)
            except Exception as err:
                # print(traceback.format_exc())
                error_type = type(err).__name__
                error_description = str(err)
                raise errors.SelectorProcessingError(
                    method_name.value, f"{error_type}: {error_description}")
            self.summary[method_name.value] = support
        result = self.summary.to_dict(orient="index")
        return schemas.FeatureSelectionSummary(result=result)

    def _validate_params(self, method_name: fs, params: Optional[Dict[str, Any]]):
        schema = self._params_map[method_name]
        if params is None:
            return schema()
        else:
            try:
                return schema(**params)
            except ValidationError as e:
                raise errors.InvalidSelectorParamsError(method_name.value, str(e))

    def _get_score_func(self) -> Callable:
        if self.task_type == specs.FeatureSelectionTaskType.CLASSIFICATION:
            return f_classif
        if self.task_type == specs.FeatureSelectionTaskType.REGRESSION:
            return f_regression
        else:
            raise errors.UnknownTaskTypeError(self.task_type)

    def _get_estimator(self, estimator: specs.BaseSklearnModels):
        if estimator == specs.BaseSklearnModels.LINEAR_REGRESSION:
            return LinearRegression()
        if estimator == specs.BaseSklearnModels.RANDOM_FOREST_REGRESSOR:
            return RandomForestRegressor()
        if estimator == specs.BaseSklearnModels.LOGISTIC_REGRESSION:
            return LogisticRegression()
        if estimator == specs.BaseSklearnModels.RANDOM_FOREST_CLASSIFIER:
            return RandomForestClassifier()
        else:
            raise errors.UnknownBaseEstimatorError(estimator)

    def _variance_threshold(self, params: schemas.VarianceThresholdParams):
        selector = VarianceThreshold(params.threshold)
        selector.fit(self.X, self.y)
        return selector.get_support()

    def _select_k_best(self, params: schemas.SelectKBestParams):
        score_func = self._get_score_func()
        selector = SelectKBest(score_func, k=params.k)
        selector.fit(self.X, self.y)
        return selector.get_support()

    def _select_percentile(self, params: schemas.SelectPercentileParams):
        score_func = self._get_score_func()
        selector = SelectPercentile(score_func, percentile=params.percentile)
        selector.fit(self.X, self.y)
        return selector.get_support()

    def _select_fpr(self, params: schemas.SelectFprFdrFweParams):
        score_func = self._get_score_func()
        selector = SelectFpr(score_func, alpha=params.alpha)
        selector.fit(self.X, self.y)
        return selector.get_support()

    def _select_fdr(self, params: schemas.SelectFprFdrFweParams):
        score_func = self._get_score_func()
        selector = SelectFdr(score_func, alpha=params.alpha)
        selector.fit(self.X, self.y)
        return selector.get_support()

    def _select_fwe(self, params: schemas.SelectFprFdrFweParams):
        score_func = self._get_score_func()
        selector = SelectFwe(score_func, alpha=params.alpha)
        selector.fit(self.X, self.y)
        return selector.get_support()

    # def _recursive_feature_elimination(self, params: schemas.RFEParams):
    #     estimator = self._get_estimator(params.estimator)
    #     selector = RFE(estimator, step=params.step,
    #                    n_features_to_select=params.n_features_to_select)
    #     selector.fit(self.X, self.y)
    #     return selector.get_support()

    def _recursive_feature_elimination(self, params: schemas.RFEParams):
        estimator = self._get_estimator(params.estimator)
        selector = RFE(estimator, step=params.step)
        selector.fit(self.X, self.y)
        return selector.ranking_

    # def _select_from_model(self, params: schemas.SelectFromModelParams):
    #     estimator = self._get_estimator(params.estimator)
    #     estimator.fit(self.X, self.y)
    #     selector = SelectFromModel(estimator, prefit=True)
    #     return selector.get_support()

    def _select_from_model(self, params: schemas.SelectFromModelParams):
        estimator = self._get_estimator(params.estimator)
        estimator.fit(self.X, self.y)
        if hasattr(estimator, 'feature_importances_'):
            feature_weights = estimator.feature_importances_
        elif hasattr(estimator, 'coef_'):
            feature_weights = estimator.coef_[0] if len(
                estimator.coef_.shape) > 1 else estimator.coef_
        else:
            feature_weights = np.zeros(self.X.shape[1])
        return feature_weights

    def _sequential_forward_selection(self, params: schemas.SfsSbsParams):
        estimator = self._get_estimator(params.estimator)
        selector = SequentialFeatureSelector(estimator, direction="forward",
            n_features_to_select=params.n_features_to_select)
        selector.fit(self.X, self.y)
        return selector.get_support()

    def _sequential_backward_selection(self, params: schemas.SfsSbsParams):
        estimator = self._get_estimator(params.estimator)
        selector = SequentialFeatureSelector(estimator, direction="backward",
            n_features_to_select=params.n_features_to_select)
        selector.fit(self.X, self.y)
        return selector.get_support()


# feature_selection_params_raw = [
#     {
#         "method_name": "variance_threshold",
#         "params": {
#             "threshold": 0.8
#         }
#     },
#     {
#         "method_name": "select_k_best",
#         "params": {
#             "score_func": "chi2",
#             "k": 4
#         }
#     },
#     {
#         "method_name": "select_percentile",
#         "params": {
#             "score_func": "f_classif",
#             "percentile": 10
#         }
#     },
#     {
#         "method_name": "select_fpr",
#         "params": {
#             "score_func": "f_classif",
#             "alpha": 0.05
#         }
#     },
#
#     {
#         "method_name": "recursive_feature_elimination",
#         "params": {
#             "estimator": "logistic_regression",
#             "n_features_to_select": 3,
#             "step": 1
#         }
#     },
#     {
#         "method_name": "select_from_model",
#         "params": {
#             "estimator": "random_forest_classifier"
#         }
#     },
#     {
#         "method_name": "sequential_forward_selection",
#         "params": {
#             "estimator": "logistic_regression",
#             "n_features_to_select": 3
#         }
#     },
#     {
#         "method_name": "sequential_backward_selection",
#         "params": {
#             "estimator": "random_forest_classifier",
#             "n_features_to_select": 3
#         }
#     }
# ]
#
# feature_selection_params = []
#
# for method_param in feature_selection_params_raw:
#     feature_selection_params.append(
#         schemas.SelectorMethodParams(**method_param))

from typing import List, Dict, Any, Callable

from pydantic import ValidationError
from sklearn.feature_selection import VarianceThreshold, SelectKBest
from sklearn.feature_selection import f_classif, f_regression
from sklearn.feature_selection import SelectPercentile, SelectFpr, SelectFdr, \
    SelectFwe, RFE, SelectFromModel, SequentialFeatureSelector
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import pandas as pd

from ml_api.apps.dataframes import schemas, specs
from ml_api.apps.dataframes.specs import FeatureSelectionMethods as fs
from ml_api.apps.dataframes.errors import WrongSelectorParamsError, \
    SelectorMethodNotExistsError, SelectorProcessingError


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

        self._methods = {
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

    def _get_score_func(self) -> Callable:
        if self.task_type == specs.FeatureSelectionTaskType.CLASSIFICATION:
            return f_classif
        if self.task_type == specs.FeatureSelectionTaskType.REGRESSION:
            return f_regression
        else:
            raise WrongSelectorParamsError("TaskType")

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
            raise WrongSelectorParamsError("Estimator")

    def _variance_threshold(self, params: Dict[str, Any]):
        method_name = fs.VARIANCE_THRESHOLD.value
        try:
            params = schemas.VarianceThresholdParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError(method_name)
        selector = VarianceThreshold(params.threshold)
        try:
            selector.fit(self.X, self.y)
        except Exception as err:
            raise SelectorProcessingError(method_name, err)
        self.summary[method_name] = selector.get_support()

    def _select_k_best(self, params: Dict[str, Any]):
        method_name = fs.SELECT_K_BEST.value
        try:
            params = schemas.SelectKBestParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError(method_name)
        score_func = self._get_score_func()
        selector = SelectKBest(score_func, k=params.k)
        try:
            selector.fit(self.X, self.y)
        except Exception as err:
            raise SelectorProcessingError(method_name, err)
        self.summary[method_name] = selector.get_support()

    def _select_percentile(self, params: Dict[str, Any]):
        method_name = fs.SELECT_PERCENTILE.value
        try:
            params = schemas.SelectPercentileParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError(method_name)
        score_func = self._get_score_func()
        selector = SelectPercentile(score_func, percentile=params.percentile)
        try:
            selector.fit(self.X, self.y)
        except Exception as err:
            raise SelectorProcessingError(method_name, err)
        self.summary[method_name] = selector.get_support()

    def _select_fpr(self, params: Dict[str, Any]):
        method_name = fs.SELECT_FPR.value
        try:
            params = schemas.SelectFprFdrFweParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError(method_name)
        score_func = self._get_score_func()
        selector = SelectFpr(score_func, alpha=params.alpha)
        try:
            selector.fit(self.X, self.y)
        except Exception as err:
            raise SelectorProcessingError(method_name, err)
        self.summary[method_name] = selector.get_support()

    def _select_fdr(self, params: Dict[str, Any]):
        method_name = fs.SELECT_FDR.value
        try:
            params = schemas.SelectFprFdrFweParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError(method_name)
        score_func = self._get_score_func()
        selector = SelectFdr(score_func, alpha=params.alpha)
        try:
            selector.fit(self.X, self.y)
        except Exception as err:
            raise SelectorProcessingError(method_name, err)
        self.summary[method_name] = selector.get_support()

    def _select_fwe(self, params: Dict[str, Any]):
        method_name = fs.SELECT_FWE.value
        try:
            params = schemas.SelectFprFdrFweParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError(method_name)
        score_func = self._get_score_func()
        selector = SelectFwe(score_func, alpha=params.alpha)
        try:
            selector.fit(self.X, self.y)
        except Exception as err:
            raise SelectorProcessingError(method_name, err)
        self.summary[method_name] = selector.get_support()

    def _recursive_feature_elimination(self, params: Dict[str, Any]):
        method_name = fs.RECURSIVE_FEATURE_ELIMINATION.value
        try:
            params = schemas.RFEParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError(method_name)
        estimator = self._get_estimator(params.estimator)
        selector = RFE(estimator,
                       n_features_to_select=params.n_features_to_select,
                       step=params.step)
        try:
            selector.fit(self.X, self.y)
        except Exception as err:
            raise SelectorProcessingError(method_name, err)
        self.summary[method_name] = selector.get_support()

    def _select_from_model(self, params: Dict[str, Any]):
        method_name = fs.SELECT_FROM_MODEL.value
        try:
            params = schemas.SelectFromModelParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError(method_name)
        estimator = self._get_estimator(params.estimator)
        try:
            estimator.fit(self.X, self.y)
        except Exception as err:
            raise SelectorProcessingError(method_name, err)
        selector = SelectFromModel(estimator, prefit=True)
        self.summary[method_name] = selector.get_support()

    def _sequential_forward_selection(self, params: Dict[str, Any]):
        method_name = fs.SEQUENTIAL_FORWARD_SELECTION.value
        try:
            params = schemas.SfsSbsParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError(method_name)
        estimator = self._get_estimator(params.estimator)
        selector = SequentialFeatureSelector(estimator, direction="forward",
            n_features_to_select=params.n_features_to_select)
        try:
            selector.fit(self.X, self.y)
        except Exception as err:
            raise SelectorProcessingError(method_name, err)
        self.summary[method_name] = selector.get_support()

    def _sequential_backward_selection(self, params: Dict[str, Any]):
        method_name = fs.SEQUENTIAL_BACKWARD_SELECTION.value
        try:
            params = schemas.SfsSbsParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError(method_name)
        estimator = self._get_estimator(params.estimator)
        selector = SequentialFeatureSelector(estimator, direction="backward",
            n_features_to_select=params.n_features_to_select)
        try:
            selector.fit(self.X, self.y)
        except Exception as err:
            raise SelectorProcessingError(method_name, err)
        self.summary[method_name] = selector.get_support()

    def get_empty_summary(self) -> schemas.FeatureSelectionSummary:
        for method_param in self.params:
            method_name = method_param.method_name
            if method_name not in self._methods:
                raise SelectorMethodNotExistsError(method_name)
            self.summary[method_name.value] = None
        result = self.summary.to_dict(orient="index")
        return schemas.FeatureSelectionSummary(result=result)

    def get_summary(self) -> schemas.FeatureSelectionSummary:
        for method_param in self.params:
            method_name = method_param.method_name
            params = method_param.params
            if method_name not in self._methods:
                raise SelectorMethodNotExistsError(method_name)
            self._methods[method_name.value](params)
        result = self.summary.to_dict(orient="index")
        return schemas.FeatureSelectionSummary(result=result)


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

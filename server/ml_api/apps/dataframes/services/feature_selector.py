from typing import List, Dict, Any, Callable

from pydantic import ValidationError
from sklearn.feature_selection import VarianceThreshold, SelectKBest
from sklearn.feature_selection import chi2, f_classif, f_regression
from sklearn.feature_selection import SelectPercentile, SelectFpr, SelectFdr, \
    SelectFwe, RFE, SelectFromModel, SequentialFeatureSelector
from sklearn.linear_model import LogisticRegression, Lasso
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import pandas as pd

from ml_api.apps.dataframes import schemas, specs
from ml_api.apps.dataframes.errors import WrongSelectorParamsError, SelectorMethodNotExistsError


class FeatureSelector:
    def __init__(self, features, target,
                 selector_params: List[schemas.SelectorMethodParams]):
        self.X = features
        self.y = target
        self.summary = pd.DataFrame(index=features.columns)
        self.params = selector_params
        self.methods = {
            specs.FeatureSelectionMethods.variance_threshold: self._variance_threshold,
            specs.FeatureSelectionMethods.select_k_best: self._select_k_best,
            specs.FeatureSelectionMethods.select_percentile: self._select_percentile,
            specs.FeatureSelectionMethods.select_fpr: self._select_fpr,
            specs.FeatureSelectionMethods.select_fdr: self._select_fdr,
            specs.FeatureSelectionMethods.select_fwe: self._select_fwe,
            specs.FeatureSelectionMethods.recursive_feature_elimination: self._recursive_feature_elimination,
            specs.FeatureSelectionMethods.select_from_model: self._select_from_model,
            specs.FeatureSelectionMethods.sequential_forward_selection: self._sequential_forward_selection,
            specs.FeatureSelectionMethods.sequential_backward_selection: self._sequential_backward_selection,
        }

    def _get_score_func(self, score_func: str) -> Callable:
        if score_func == specs.ScoreFunc.chi2:
            return chi2
        if score_func == specs.ScoreFunc.f_classif:
            return f_classif
        if score_func == specs.ScoreFunc.f_regression:
            return f_regression
        else:
            raise WrongSelectorParamsError("ScoreFunc")

    def _get_estimator(self, estimator: specs.BaseSklearnModels):
        if estimator == specs.BaseSklearnModels.linear_regression:
            return Lasso()
        if estimator == specs.BaseSklearnModels.random_forest_regressor:
            return RandomForestRegressor()
        if estimator == specs.BaseSklearnModels.logistic_regression:
            return LogisticRegression()
        if estimator == specs.BaseSklearnModels.linear_svc:
            return LinearSVC(penalty="l1")
        if estimator == specs.BaseSklearnModels.random_forest_classifier:
            return RandomForestClassifier()
        else:
            raise WrongSelectorParamsError("Estimator")

    def _variance_threshold(self, params: Dict[str, Any]):
        try:
            params = schemas.VarianceThresholdParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("VarianceThreshold")
        selector = VarianceThreshold(params.threshold)
        selector.fit(self.X)
        self.summary["VarianceThreshold"] = selector.get_support()

    def _select_k_best(self, params: Dict[str, Any]):
        try:
            params = schemas.SelectKBestParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("SelectKBest")
        score_func = self._get_score_func(params.score_func)
        selector = SelectKBest(score_func, k=params.k)
        selector.fit(self.X, self.y)
        self.summary["SelectKBest"] = selector.get_support()

    def _select_percentile(self, params: Dict[str, Any]):
        try:
            params = schemas.SelectPercentileParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("SelectPercentile")
        score_func = self._get_score_func(params.score_func)
        selector = SelectPercentile(score_func, percentile=params.percentile)
        selector.fit(self.X, self.y)
        self.summary["SelectPercentile"] = selector.get_support()

    def _select_fpr(self, params: Dict[str, Any]):
        try:
            params = schemas.SelectFprFdrFweParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("SelectFpr")
        score_func = self._get_score_func(params.score_func)
        selector = SelectFpr(score_func, alpha=params.alpha)
        selector.fit(self.X, self.y)
        self.summary["SelectFpr"] = selector.get_support()

    def _select_fdr(self, params: Dict[str, Any]):
        try:
            params = schemas.SelectFprFdrFweParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("SelectFdr")
        score_func = self._get_score_func(params.score_func)
        selector = SelectFdr(score_func, alpha=params.alpha)
        selector.fit(self.X, self.y)
        self.summary["SelectFdr"] = selector.get_support()

    def _select_fwe(self, params: Dict[str, Any]):
        try:
            params = schemas.SelectFprFdrFweParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("SelectFwe")
        score_func = self._get_score_func(params.score_func)
        selector = SelectFwe(score_func, alpha=params.alpha)
        selector.fit(self.X, self.y)
        self.summary["SelectFwe"] = selector.get_support()

    def _recursive_feature_elimination(self, params: Dict[str, Any]):
        try:
            params = schemas.RFEParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("RecursiveFeatureElimination")
        estimator = self._get_estimator(params.estimator)
        selector = RFE(estimator,
                       n_features_to_select=params.n_features_to_select,
                       step=params.step)
        try:
            selector.fit(self.X, self.y)
        except ValueError:
            raise WrongSelectorParamsError("SelectFromModel")
        self.summary["RecursiveFeatureElimination"] = selector.get_support()

    def _select_from_model(self, params: Dict[str, Any]):
        try:
            params = schemas.SelectFromModelParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("SelectFromModel")
        estimator = self._get_estimator(params.estimator)
        try:
            estimator.fit(self.X, self.y)
        except ValueError:
            raise WrongSelectorParamsError("SelectFromModel")
        selector = SelectFromModel(estimator, prefit=True)
        self.summary["SelectFromModel"] = selector.get_support()
        return self

    def _sequential_forward_selection(self, params: Dict[str, Any]):
        try:
            params = schemas.SfsSbsParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("SequentialForwardSelection")
        estimator = self._get_estimator(params.estimator)
        selector = SequentialFeatureSelector(estimator, direction="forward",
            n_features_to_select=params.n_features_to_select)
        selector.fit(self.X, self.y)
        self.summary["SequentialForwardSelection"] = selector.get_support()
        return self

    def _sequential_backward_selection(self, params: Dict[str, Any]):
        try:
            params = schemas.SfsSbsParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("SequentialBackwardSelection")
        estimator = self._get_estimator(params.estimator)
        selector = SequentialFeatureSelector(estimator, direction="backward",
            n_features_to_select=params.n_features_to_select)
        selector.fit(self.X, self.y)
        self.summary["SequentialBackwardSelection"] = selector.get_support()
        return self

    def get_summary(self):
        for method_param in self.params:
            method_name = method_param.method_name
            params = method_param.params
            if method_name not in self.methods:
                raise SelectorMethodNotExistsError(method_name)
            self.methods[method_name](params)
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

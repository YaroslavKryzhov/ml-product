from typing import List, Dict, Any, Callable

from pydantic import ValidationError
from sklearn.feature_selection import VarianceThreshold, SelectKBest
from sklearn.feature_selection import chi2, f_classif, f_regression
from sklearn.feature_selection import SelectPercentile, SelectFpr, SelectFdr, SelectFwe, RFE, SelectFromModel
from sklearn.linear_model import LogisticRegression
import pandas as pd

from ml_api.apps.dataframes import schemas, specs
from ml_api.apps.dataframes.errors import WrongSelectorParamsError, SelectorMethodNotExistsError


class FeatureSelector:
    def __init__(self, features, target,
                 selector_params: List[schemas.SelectorMethodParams]):
        # TODO: finish this class
        self.X = features
        self.y = target
        self.summary = pd.DataFrame(index=features.columns)
        self.params = selector_params
        self.methods = {
            "variance_threshold": self._variance_threshold,
            "select_k_best": self._select_k_best,
            "select_percentile": self._select_percentile,
            "select_fpr": self._select_fpr,
            "select_fdr": self._select_fdr,
            "select_fwe": self._select_fwe,
            # "rfe": self._recursive_feature_elimination,
            # "select_from_model": self._select_from_model,
        }

    def _get_score_func(self, score_func: str) -> Callable:
        if score_func == specs.ScoreFunc.chi2:
            return chi2
        if score_func == specs.ScoreFunc.f_classif:
            return f_classif
        if score_func == specs.ScoreFunc.f_regression:
            return f_regression

    def _variance_threshold(self, params: Dict[str, Any]):
        try:
            params = schemas.VarianceThresholdParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("VarianceThreshold")
        selector = VarianceThreshold(params.threshold)
        selector.fit(self.X)
        self.summary["VarianceThreshold"] = selector.get_support()
        return self

    def _select_k_best(self, params: Dict[str, Any]):
        try:
            params = schemas.SelectKBestParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("SelectKBest")
        score_func = self._get_score_func(params.score_func)
        selector = SelectKBest(score_func, k=params.k)
        selector.fit(self.X, self.y)
        self.summary["SelectKBest"] = selector.get_support()
        return self

    def _select_percentile(self, params: Dict[str, Any]):
        try:
            params = schemas.SelectPercentileParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("SelectPercentile")
        score_func = self._get_score_func(params.score_func)
        selector = SelectPercentile(score_func, percentile=params.percentile)
        selector.fit(self.X, self.y)
        self.summary["SelectPercentile"] = selector.get_support()
        return self

    def _select_fpr(self, params: Dict[str, Any]):
        try:
            params = schemas.SelectFprFdrFweParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("SelectFpr")
        score_func = self._get_score_func(params.score_func)
        selector = SelectFpr(score_func, alpha=params.alpha)
        selector.fit(self.X, self.y)
        self.summary["SelectFpr"] = selector.get_support()
        return self

    def _select_fdr(self, params: Dict[str, Any]):
        try:
            params = schemas.SelectFprFdrFweParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("SelectFdr")
        score_func = self._get_score_func(params.score_func)
        selector = SelectFdr(score_func, alpha=params.alpha)
        selector.fit(self.X, self.y)
        self.summary["SelectFdr"] = selector.get_support()
        return self

    def _select_fwe(self, params: Dict[str, Any]):
        try:
            params = schemas.SelectFprFdrFweParams(**params)
        except ValidationError:
            raise WrongSelectorParamsError("SelectFwe")
        score_func = self._get_score_func(params.score_func)
        selector = SelectFwe(score_func, alpha=params.alpha)
        selector.fit(self.X, self.y)
        self.summary["SelectFwe"] = selector.get_support()
        return self

    # def _recursive_feature_elimination(self, params: Dict[str, Any]):
    #     try:
    #         params = schemas.RFEParams(**params)
    #     except ValidationError:
    #         raise WrongSelectorParamsError("RecursiveFeatureElimination")
    #     model = LogisticRegression()
    #     selector = RFE(model, params.n_features_to_select, step=params.step)
    #     selector.fit(self.X, self.y)
    #     self.summary["RecursiveFeatureElimination"] = selector.get_support()
    #     return self
    #
    # def _select_from_model(self, params: Dict[str, Any]):
    #     try:
    #         params = schemas.SelectFromModelParams(**params)
    #     except ValidationError:
    #         raise WrongSelectorParamsError("SelectFromModel")
    #     model = RandomForestClassifier()
    #     model.fit(self.X, self.y)
    #     selector = SelectFromModel(model, threshold=params.threshold,
    #                                prefit=True)
    #     self.summary["SelectFromModel"] = selector.get_support()
    #     return self

    # Sequential Forward Selection (SFS) и Sequential Backward Selection (SBS) не являются частью sklearn
    # Можно использовать mlxtend библиотеку, но мы пропустим эти методы в этом примере

    def get_summary(self):
        for method_param in self.params:
            method_name = method_param.method_name
            params = method_param.params
            if method_name not in self.methods:
                raise SelectorMethodNotExistsError(method_name)
            self.methods[method_name](params)
        result = self.summary.to_dict(orient="index")
        return schemas.FeatureSelectionSummary(result=result)


from typing import List, Dict, Union, Optional, Any

from pydantic import BaseModel
from ml_api.apps.dataframes.specs import ScoreFunc, FeatureSelectionMethods


class NumericColumnDescription(BaseModel):
    count: int
    mean: float
    std: float
    min: float
    first_percentile: float
    second_percentile: float
    third_percentile: float
    max: float


class CategoricalColumnDescription(BaseModel):
    nunique: int
    most_frequent: Dict[str, int]


class ColumnDescription(BaseModel):
    name: str
    type: str
    data_type: str
    not_null_count: int
    null_count: int
    data: List[Dict]
    column_stats: Union[NumericColumnDescription, CategoricalColumnDescription]


class ReadDataFrameResponse(BaseModel):
    total: int
    records: Dict[str, List]


class SelectorMethodParams(BaseModel):
    method_name: FeatureSelectionMethods
    params: Optional[Dict[str, Any]] = None


class FeatureSelectionSummary:
    result: Dict[str, Dict[str, bool]]


class VarianceThresholdParams(BaseModel):
    threshold: Optional[float] = 0


class SelectKBestParams(BaseModel):
    score_func: ScoreFunc
    k: Union[int, "all"]


class SelectPercentileParams(BaseModel):
    score_func: ScoreFunc
    percentile: int


class SelectFprFdrFweParams(BaseModel):
    score_func: ScoreFunc
    alpha: float


class RFEParams(BaseModel):
    estimator: str
    n_features_to_select: Optional[int]
    step: Union[int, float]


class SFSParams(BaseModel):
    estimator: str
    k_features: Union[int, tuple, str]
    forward: bool
    floating: bool


class SBSParams(BaseModel):
    estimator: str
    k_features: Union[int, tuple, str]
    forward: bool
    floating: bool


class SelectFromModelParams(BaseModel):
    estimator: str
    threshold: Optional[str]

from typing import List, Dict, Union, Optional, Any

from pydantic import BaseModel, Field
from ml_api.apps.dataframes.specs import ScoreFunc, FeatureSelectionMethods, \
    BaseSklearnModels


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


class FeatureSelectionSummary(BaseModel):
    result: Dict[str, Dict[str, bool]]


class VarianceThresholdParams(BaseModel):
    threshold: Optional[float] = Field(0, ge=0)  # threshold should be greater than or equal to 0


class SelectKBestParams(BaseModel):
    score_func: ScoreFunc
    k: int = Field(1, ge=1)  # k should be greater than or equal to 1


class SelectPercentileParams(BaseModel):
    score_func: ScoreFunc
    percentile: int = Field(10, ge=1, le=100)  # percentile should be between 1 and 100


class SelectFprFdrFweParams(BaseModel):
    score_func: ScoreFunc
    alpha: float = Field(0.05, ge=0, le=1)  # alpha should be between 0 and 1


class RFEParams(BaseModel):
    estimator: BaseSklearnModels = BaseSklearnModels.linear_regression
    n_features_to_select: Optional[int] = Field(None, ge=1)  # n_features_to_select should be greater than or equal to 1
    step: Optional[int] = Field(1, ge=1)  # step should be greater than or equal to 1


class SelectFromModelParams(BaseModel):
    estimator: BaseSklearnModels = BaseSklearnModels.linear_regression


class SfsSbsParams(BaseModel):
    estimator: BaseSklearnModels = BaseSklearnModels.linear_regression
    n_features_to_select: int = Field(1, ge=1)  # n_features_to_select should be greater than or equal to 1

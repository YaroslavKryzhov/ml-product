from typing import List, Dict, Union, Optional, Any

from pydantic import BaseModel, Field
from ml_api.apps.dataframes.specs import FeatureSelectionMethods, \
    BaseSklearnModels, AvailableMethods, ColumnType


class ColumnTypes(BaseModel):
    numeric: List[str]
    categorical: List[str]


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
    result: Dict[str, Dict[str, Optional[Any]]]


class VarianceThresholdParams(BaseModel):
    threshold: Optional[float] = Field(0, ge=0)


class SelectKBestParams(BaseModel):
    k: int = Field(1, ge=1)


class SelectPercentileParams(BaseModel):
    percentile: int = Field(10, ge=1, le=100)


class SelectFprFdrFweParams(BaseModel):
    alpha: float = Field(0.05, ge=0, le=1)


class RFEParams(BaseModel):
    estimator: BaseSklearnModels = BaseSklearnModels.LINEAR_REGRESSION
    n_features_to_select: Optional[int] = Field(None, ge=1)
    step: Optional[int] = Field(1, ge=1)


class SelectFromModelParams(BaseModel):
    estimator: BaseSklearnModels = BaseSklearnModels.LINEAR_REGRESSION


class SfsSbsParams(BaseModel):
    estimator: BaseSklearnModels = BaseSklearnModels.LINEAR_REGRESSION
    n_features_to_select: int = Field(1, ge=1)


class ApplyMethodParams(BaseModel):
    method_name: AvailableMethods
    columns: Optional[List[str]] = None
    params: Optional[Dict[str, Any]] = None


class ChangeColumnsTypeParams(BaseModel):
    new_type: ColumnType


class FillCustomValueParams(BaseModel):
    values_to_fill: List[Union[int, float, str]]


class LeaveNValuesParams(BaseModel):
    values_to_keep: List[List[str]]


class OneHotEncoderParams(BaseModel):
    categories_: List[List[Union[str]]]
    drop_idx_: Optional[List[int]]
    infrequent_enabled: bool
    n_features_outs: List[int]


class OrdinalEncodingParams(BaseModel):
    categories_: List[List[Union[str]]]
    missing_indices: Dict


class StandardScalerParams(BaseModel):
    mean_: List[float]
    scale_: List[float]


class MinMaxScalerParams(BaseModel):
    min_: List[float]
    scale_: List[float]


class RobustScalerParams(BaseModel):
    center_: List[float]
    scale_: List[float]

from typing import List, Dict, Union

from pydantic import BaseModel


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

from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

from ml_api.apps.dataframes.specs import AvailableFunctions


class ColumnDescription(BaseModel):
    name: str
    type: str
    not_null_count: int
    data_type: str
    data: List[Dict]


class ReadDataFrameResponse(BaseModel):
    total: int
    records: Dict[str, List]


class DataFrameDescription(BaseModel):
    count: Dict
    mean: Dict
    std: Dict
    min: Dict
    first_percentile: Dict
    second_percentile: Dict
    third_percentile: Dict
    max: Dict


class PipelineElement(BaseModel):
    function_name: AvailableFunctions
    params: Any = None


class ColumnTypes(BaseModel):
    numeric: List[str]
    categorical: List[str]
    target: Optional[str] = None


class DataFrameInfo(BaseModel):
    id: UUID
    filename: str
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    pipeline: List[PipelineElement]
    column_types: Optional[ColumnTypes]

    class Config:
        orm_mode = True

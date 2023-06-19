from datetime import datetime
from typing import List, Any, Optional

from pydantic import BaseModel, Field
from beanie import Document
from beanie.odm.fields import PydanticObjectId

from ml_api.apps.dataframes.specs import AvailableFunctions


class ColumnTypes(BaseModel):
    numeric: List[str]
    categorical: List[str]


class PipelineElement(BaseModel):
    function_name: AvailableFunctions
    params: Any = None


class DataFrameMetadata(Document):
    parent_id: Optional[PydanticObjectId] = None
    filename: str
    user_id: PydanticObjectId
    feature_columns_types: Optional[ColumnTypes] = None
    target_feature: Optional[str] = None
    pipeline: Optional[List[PipelineElement]] = []
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    class Settings:
        collection = "dataframe_collection"

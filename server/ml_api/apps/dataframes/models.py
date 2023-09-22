from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from beanie import Document
from beanie.odm.fields import PydanticObjectId
from pymongo import IndexModel, ASCENDING, HASHED

from ml_api.apps.dataframes.schemas import ApplyMethodParams, FeatureSelectionSummary


class ColumnTypes(BaseModel):
    numeric: List[str]
    categorical: List[str]


class DataFrameMetadata(Document):
    parent_id: Optional[PydanticObjectId] = None
    filename: str
    user_id: PydanticObjectId
    is_prediction: bool = False
    feature_columns_types: Optional[ColumnTypes] = ColumnTypes(
        numeric=[], categorical=[])
    target_feature: Optional[str] = None
    pipeline: Optional[List[ApplyMethodParams]] = []
    feature_importance_report: FeatureSelectionSummary = None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    class Settings:
        collection = "dataframe_collection"
        indexes = [
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("user_id", ASCENDING), (
                "filename", ASCENDING)], unique=True),
            IndexModel([("parent_id", HASHED)]),
        ]

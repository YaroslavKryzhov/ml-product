from datetime import datetime
from typing import List, Optional

from pydantic import Field
from bunnet import Document
from bunnet import PydanticObjectId
from pymongo import IndexModel, ASCENDING, HASHED

from ml_api.apps.dataframes import schemas


class DataFrameMetadata(Document):
    parent_id: Optional[PydanticObjectId] = None
    filename: str
    user_id: PydanticObjectId
    is_prediction: bool = False
    feature_columns_types: Optional[schemas.ColumnTypes] = schemas.ColumnTypes(
        numeric=[], categorical=[])
    target_feature: Optional[str] = None
    pipeline: Optional[List[schemas.ApplyMethodParams]] = []
    feature_importance_report: Optional[schemas.FeatureSelectionSummary] = None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    class Settings:
        collection = "dataframe_collection"
        indexes = [
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("user_id", ASCENDING), (
                "filename", ASCENDING)], unique=True),
            IndexModel([("parent_id", HASHED)]),
        ]

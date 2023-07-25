from datetime import datetime
from typing import List, Optional, Dict

from beanie import Document
from beanie.odm.fields import PydanticObjectId
from pymongo import IndexModel, ASCENDING, HASHED
from pydantic import Field

from ml_api.apps.ml_models.specs import AvailableTaskTypes, AvailableCompositionTypes
from ml_api.apps.ml_models.schemas import ModelParams, ModelStatuses


class CompositionMetadata(Document):
    filename: str
    user_id: PydanticObjectId
    dataframe_id: PydanticObjectId
    task_type: Optional[AvailableTaskTypes] = None
    composition_type: AvailableCompositionTypes
    composition_params: ModelParams
    features: Optional[List[str]] = []
    target: Optional[str] = None
    status: ModelStatuses = ModelStatuses.BUILDING
    metrics_report: Optional[Dict[float]] = None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    class Settings:
        collection = "composition_collection"
        indexes = [
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("user_id", ASCENDING), (
                "filename", ASCENDING)], unique=True),
            IndexModel([("dataframe_id", HASHED)]),
        ]
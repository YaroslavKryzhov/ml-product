from datetime import datetime
from typing import List, Optional

from beanie import Document
from beanie.odm.fields import PydanticObjectId
from pymongo import IndexModel, ASCENDING, HASHED
from pydantic import Field

from ml_api.apps.ml_models import specs
from ml_api.apps.ml_models.schemas import ModelParams


class ModelMetadata(Document):
    filename: str
    user_id: PydanticObjectId
    dataframe_id: PydanticObjectId
    task_type: specs.AvailableTaskTypes
    model_params: ModelParams
    params_type: specs.AvailableParamsTypes
    feature_columns: Optional[List[str]] = []
    target_column: Optional[str] = None
    test_size: Optional[float] = 0.25
    stratify: Optional[bool] = False
    status: specs.ModelStatuses = specs.ModelStatuses.BUILDING
    metrics_report_ids: List[PydanticObjectId] = []
    model_prediction_ids: List[PydanticObjectId] = []
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    class Settings:
        collection = "model_collection"
        indexes = [
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("user_id", ASCENDING), (
                "filename", ASCENDING)], unique=True),
            IndexModel([("dataframe_id", HASHED)]),
        ]

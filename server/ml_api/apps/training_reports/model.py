from datetime import datetime
from typing import Dict

from bunnet import Document
from bunnet import PydanticObjectId
from pymongo import IndexModel, ASCENDING, HASHED
from pydantic import Field

from ml_api.apps.ml_models.specs import AvailableTaskTypes
from ml_api.apps.training_reports.specs import ReportTypes


class Report(Document):
    user_id: PydanticObjectId = None
    model_id: PydanticObjectId = None
    dataframe_id: PydanticObjectId = None
    task_type: AvailableTaskTypes = None
    report_type: ReportTypes = None
    body: Dict = None

    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    class Settings:
        collection = "report_collection"
        indexes = [
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("dataframe_id", HASHED)]),
            IndexModel([("model_id", HASHED)]),
        ]

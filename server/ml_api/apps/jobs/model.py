from datetime import datetime
from typing import Dict

from bunnet import Document
from bunnet import PydanticObjectId
from pymongo import IndexModel, ASCENDING
from pydantic import Field

from ml_api.apps.jobs import specs


class BackgroundJob(Document):
    user_id: PydanticObjectId = None
    type: specs.AvailableJobTypes = None
    object_type: specs.AvailableObjectTypes = None
    object_id: PydanticObjectId = None
    status: specs.JobStatuses = specs.JobStatuses.WAITING
    input_params: Dict = None
    output_message: str = None

    started_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    finished_at: str = None

    class Settings:
        collection = "jobs_collection"
        indexes = [
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("user_id", ASCENDING), ("object_type", ASCENDING),
                        ("object_id", ASCENDING)])
        ]

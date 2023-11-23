from fastapi import HTTPException, status
from bunnet import PydanticObjectId


class JobNotFoundError(HTTPException):
    """Raise when job not found in database"""
    def __init__(self, job_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"background job with id {job_id} not found."
        )

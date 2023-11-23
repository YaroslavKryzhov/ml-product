from fastapi import HTTPException, status
from bunnet import PydanticObjectId


class ReportNotFoundError(HTTPException):
    """Raise when report not found in database"""
    def __init__(self, report_id: PydanticObjectId):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report with id {report_id} not found."
        )

from typing import List

from beanie import PydanticObjectId

from ml_api.apps.training_reports.models import Report
from ml_api.apps.training_reports.errors import ReportNotFoundError


class TrainingReportCRUD:
    def __init__(self, user_id: PydanticObjectId):
        self.user_id = user_id

    async def save(self, report: Report) -> Report:
        await report.insert()
        return report

    async def get(self, report_id: PydanticObjectId) -> Report:
        report = await Report.get(report_id)
        if report is None:
            raise ReportNotFoundError(report_id)
        return report

    async def get_by_dataframe_id(self, dataframe_id: PydanticObjectId
                                  ) -> List[Report]:
        reports = await Report.find(
            Report.user_id == self.user_id).find(
            Report.dataframe_id == dataframe_id).to_list()
        return reports

    async def get_by_model_id(self, model_id: PydanticObjectId
                                  ) -> List[Report]:
        reports = await Report.find(
            Report.user_id == self.user_id).find(
            Report.model_id == model_id).to_list()
        return reports

    async def delete(self, report_id: PydanticObjectId) -> Report:
        report = await Report.get(report_id)
        if report is None:
            raise ReportNotFoundError(report)
        return await report.delete()

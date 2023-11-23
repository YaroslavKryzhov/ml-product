from typing import List

from bunnet import PydanticObjectId

from ml_api.apps.training_reports.model import Report
from ml_api.apps.training_reports.errors import ReportNotFoundError


class TrainingReportCRUD:
    def __init__(self, user_id: PydanticObjectId):
        self.user_id = user_id

    def save(self, report: Report) -> Report:
        report.insert()
        return report

    def get(self, report_id: PydanticObjectId) -> Report:
        report = Report.get(report_id).run()
        if report is None:
            raise ReportNotFoundError(report_id)
        return report

    def get_by_dataframe_id(self, dataframe_id: PydanticObjectId
                                  ) -> List[Report]:
        reports = Report.find(
            Report.user_id == self.user_id).find(
            Report.dataframe_id == dataframe_id).to_list()
        return reports

    def get_by_model_id(self, model_id: PydanticObjectId
                                  ) -> List[Report]:
        reports = Report.find(
            Report.user_id == self.user_id).find(
            Report.model_id == model_id).to_list()
        return reports

    def delete(self, report_id: PydanticObjectId) -> Report:
        report = Report.get(report_id).run()
        if report is None:
            raise ReportNotFoundError(report)
        return report.delete()

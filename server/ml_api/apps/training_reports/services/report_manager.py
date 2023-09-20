from typing import List

from beanie import PydanticObjectId

from ml_api.apps.training_reports.models import Report
from ml_api.apps.training_reports.repository import TrainingReportCRUD


class ReportManagerService:
    """
    Работает с данными в MongoDB, обеспечивает доступ
    и управление отчетами об обучении.
    """

    def __init__(self, user_id):
        self._user_id = user_id
        self.report_repository = TrainingReportCRUD(self._user_id)

    async def save_report(self, model_id: PydanticObjectId,
                          dataframe_id: PydanticObjectId,
                          report: Report) -> Report:
        report.user_id = self._user_id
        report.model_id = model_id
        report.dataframe_id = dataframe_id
        return await self.report_repository.save(report)

    async def get_report(self, report_id: PydanticObjectId) -> Report:
        return await self.report_repository.get(report_id)

    async def get_reports_by_dataframe_id(self, dataframe_id: PydanticObjectId
                                          ) -> List[Report]:
        return await self.report_repository.get_by_dataframe_id(dataframe_id)

    async def get_reports_by_model_id(self, model_id: PydanticObjectId
                                          ) -> List[Report]:
        return await self.report_repository.get_by_model_id(model_id)

    async def delete_report(self, report_id: PydanticObjectId
                                          ) -> List[Report]:
        return await self.report_repository.delete(report_id)

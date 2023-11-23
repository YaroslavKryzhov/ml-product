from typing import List, Dict

from bunnet import PydanticObjectId

from ml_api.apps.jobs.model import BackgroundJob
from ml_api.apps.jobs import specs
from ml_api.apps.jobs.errors import JobNotFoundError


class BackgroundJobsCRUD:
    def __init__(self, user_id: PydanticObjectId):
        self.user_id = user_id

    def add(self, job: BackgroundJob) -> BackgroundJob:
        job.insert()
        return job

    def get(self, job_id: PydanticObjectId) -> BackgroundJob:
        job = BackgroundJob.get(job_id).run()
        if job is None:
            raise JobNotFoundError(job_id)
        return job

    def get_by_object(self,
                           object_type: specs.AvailableObjectTypes,
                           object_id: PydanticObjectId
                            ) -> List[BackgroundJob]:
        reports = BackgroundJob.find(
            BackgroundJob.user_id == self.user_id).find(
            BackgroundJob.object_type == object_type).find(
            BackgroundJob.object_id == object_id).to_list()
        return reports

    def get_all(self) -> List[BackgroundJob]:
        reports = BackgroundJob.find(
            BackgroundJob.user_id == self.user_id).to_list()
        return reports

    def update(self, job_id: PydanticObjectId,
                     query: Dict):
        job = BackgroundJob.get(job_id).run()
        if not job:
            raise JobNotFoundError(job_id)
        job.update(query)
        job_updated = BackgroundJob.get(job_id).run()
        return job_updated

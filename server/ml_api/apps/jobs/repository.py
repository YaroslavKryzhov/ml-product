from typing import List, Dict

from beanie import PydanticObjectId

from ml_api.apps.jobs.model import BackgroundJob
from ml_api.apps.jobs import specs
from ml_api.apps.jobs.errors import JobNotFoundError


class BackgroundJobsCRUD:
    def __init__(self, user_id: PydanticObjectId):
        self.user_id = user_id

    async def add(self, job: BackgroundJob) -> BackgroundJob:
        await job.insert()
        return job

    async def get(self, job_id: PydanticObjectId) -> BackgroundJob:
        job = await BackgroundJob.get(job_id)
        if job is None:
            raise JobNotFoundError(job_id)
        return job

    async def get_by_object(self,
                           object_type: specs.AvailableObjectTypes,
                           object_id: PydanticObjectId
                            ) -> List[BackgroundJob]:
        reports = await BackgroundJob.find(
            BackgroundJob.user_id == self.user_id).find(
            BackgroundJob.object_type == object_type).find(
            BackgroundJob.object_id == object_id).to_list()
        return reports

    async def get_all(self) -> List[BackgroundJob]:
        reports = await BackgroundJob.find(
            BackgroundJob.user_id == self.user_id).to_list()
        return reports

    async def update(self, job_id: PydanticObjectId,
                     query: Dict):
        job = await BackgroundJob.get(job_id)
        if not job:
            raise JobNotFoundError(job_id)
        await job.update(query)
        job_updated = await BackgroundJob.get(job_id)
        return job_updated

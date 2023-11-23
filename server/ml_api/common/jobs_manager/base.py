from bunnet import PydanticObjectId
from fastapi import HTTPException

from ml_api.apps.jobs.services import BackgroundJobsService
from ml_api.apps.jobs.model import BackgroundJob
from ml_api.common.pubsub.client import PubSub, get_pubsub_client


class JobsManager:
    def __init__(self, user_id: PydanticObjectId):
        self._user_id: PydanticObjectId = user_id
        self.pubsub: PubSub = get_pubsub_client()
        self.job_service = BackgroundJobsService(self._user_id)

    def _publish_job(self, job_info: BackgroundJob):
        self.pubsub.publish_to_channel(job_info)

    def _process_http_exception(self, err: HTTPException,
                                      job: BackgroundJob):
        # print(traceback.format_exc())
        error_type = type(err).__name__
        error_description = str(err.detail)
        message = f"{error_type}: {error_description}"
        job_info = self.job_service.error_job(job.id, message)
        return job_info

    def _process_exception(self, err: Exception, job: BackgroundJob):
        # print(traceback.format_exc())
        error_type = type(err).__name__
        error_description = str(err)
        message = f"{error_type}: {error_description}"
        job_info = self.job_service.error_job(job.id, message)
        return job_info

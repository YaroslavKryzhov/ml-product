from datetime import datetime
from typing import List, Dict

from bunnet import PydanticObjectId

from ml_api.apps.jobs.repository import BackgroundJobsCRUD
from ml_api.apps.jobs.model import BackgroundJob
from ml_api.apps.jobs import specs


class BackgroundJobsService:
    def __init__(self, user_id):
        self._user_id = user_id
        self.repository = BackgroundJobsCRUD(self._user_id)

    def get(self, job_id: PydanticObjectId) -> BackgroundJob:
        return self.repository.get(job_id)

    def get_all(self) -> List[BackgroundJob]:
        return self.repository.get_all()

    def get_by_object(self,
                      object_type: specs.AvailableObjectTypes,
                      object_id: PydanticObjectId
                      ) -> List[BackgroundJob]:
        return self.repository.get_by_object(object_type, object_id)

    def create_apply_changing_methods_job(self,
                                          dataframe_id: PydanticObjectId,
                                          input_params: Dict
                                          ) -> BackgroundJob:
        job = BackgroundJob(
            user_id=self._user_id,
            type=specs.AvailableJobTypes.APPLY_METHODS,
            object_type=specs.AvailableObjectTypes.DATAFRAME,
            object_id=dataframe_id,
            input_params=input_params
        )
        job = self.repository.add(job)
        return job

    def create_feature_importances_job(self,
                                       dataframe_id: PydanticObjectId,
                                       input_params: Dict
                                       ) -> BackgroundJob:
        job = BackgroundJob(
            user_id=self._user_id,
            type=specs.AvailableJobTypes.FEATURE_IMPORTANCES,
            object_type=specs.AvailableObjectTypes.DATAFRAME,
            object_id=dataframe_id,
            input_params=input_params
        )
        job = self.repository.add(job)
        return job

    def create_train_model_job(self,
                               model_id: PydanticObjectId,
                               input_params: Dict
                               ) -> BackgroundJob:
        job = BackgroundJob(
            user_id=self._user_id,
            type=specs.AvailableJobTypes.TRAIN_MODEL,
            object_type=specs.AvailableObjectTypes.MODEL,
            object_id=model_id,
            input_params=input_params
        )
        job = self.repository.add(job)
        return job

    def create_build_composition_job(self,
                                     composition_id: PydanticObjectId,
                                     input_params: Dict
                                     ) -> BackgroundJob:
        job = BackgroundJob(
            user_id=self._user_id,
            type=specs.AvailableJobTypes.BUILD_COMPOSITION,
            object_type=specs.AvailableObjectTypes.MODEL,
            object_id=composition_id,
            input_params=input_params
        )
        job = self.repository.add(job)
        return job

    def create_prediction_job(self,
                              model_id: PydanticObjectId,
                              input_params: Dict
                              ) -> BackgroundJob:
        job = BackgroundJob(
            user_id=self._user_id,
            type=specs.AvailableJobTypes.PREDICT_ON_MODEL,
            object_type=specs.AvailableObjectTypes.MODEL,
            object_id=model_id,
            input_params=input_params
        )
        job = self.repository.add(job)
        return job

    def run_job(self,
                job_id: PydanticObjectId,
                ) -> BackgroundJob:
        query = {"$set": {
            BackgroundJob.status: specs.JobStatuses.RUNNING
        }}
        job = self.repository.update(job_id, query)
        return job

    def complete_job(self,
                     job_id: PydanticObjectId,
                     ) -> BackgroundJob:
        output_message = "Job completed successfully"
        query = {"$set": {
            BackgroundJob.status: specs.JobStatuses.COMPLETE,
            BackgroundJob.output_message: output_message,
            BackgroundJob.finished_at: datetime.now().isoformat()
        }}
        job = self.repository.update(job_id, query)
        return job

    def error_job(self,
                  job_id: PydanticObjectId,
                  output_message: str
                  ) -> BackgroundJob:
        query = {"$set": {
            BackgroundJob.status: specs.JobStatuses.ERROR,
            BackgroundJob.output_message: output_message,
            BackgroundJob.finished_at: datetime.now().isoformat()
        }}
        job = self.repository.update(job_id, query)
        return job

from datetime import datetime
from typing import List, Dict

from beanie import PydanticObjectId

from ml_api.apps.jobs.repository import BackgroundJobsCRUD
from ml_api.apps.jobs.model import BackgroundJob
from ml_api.apps.jobs import specs


class BackgroundJobsService:
    def __init__(self, user_id):
        self._user_id = user_id
        self.repository = BackgroundJobsCRUD(self._user_id)

    async def get(self, job_id: PydanticObjectId) -> BackgroundJob:
        return await self.repository.get(job_id)

    async def get_all(self) -> List[BackgroundJob]:
        return await self.repository.get_all()

    async def get_by_object(self,
                            object_type: specs.AvailableObjectTypes,
                            object_id: PydanticObjectId
                            ) -> List[BackgroundJob]:
        return await self.repository.get_by_object(object_type, object_id)

    async def start_apply_changing_methods(self,
                                           dataframe_id: PydanticObjectId,
                                           input_params: Dict
                                           ) -> BackgroundJob:
        job = BackgroundJob(
            user_id=self._user_id,
            type=specs.AvailableJobTypes.APPLY_METHOD,
            object_type=specs.AvailableObjectTypes.DATAFRAME,
            object_id=dataframe_id,
            input_params=input_params
        )
        job = await self.repository.add(job)
        return job

    async def start_feature_importances(self,
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
        job = await self.repository.add(job)
        return job

    async def start_copy_pipeline(self,
                                  dataframe_id: PydanticObjectId,
                                  input_params: Dict
                                  ) -> BackgroundJob:
        job = BackgroundJob(
            user_id=self._user_id,
            type=specs.AvailableJobTypes.COPY_PIPELINE,
            object_type=specs.AvailableObjectTypes.DATAFRAME,
            object_id=dataframe_id,
            input_params=input_params
        )
        job = await self.repository.add(job)
        return job

    async def start_train_model(self,
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
        job = await self.repository.add(job)
        return job

    async def start_build_composition(self,
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
        job = await self.repository.add(job)
        return job

    async def start_prediction(self,
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
        job = await self.repository.add(job)
        return job

    async def complete(self,
                       job_id: PydanticObjectId,
                       ) -> BackgroundJob:
        output_message = "Job completed successfully"
        query = {"$set": {
            BackgroundJob.status: specs.JobStatuses.COMPLETE,
            BackgroundJob.output_message: output_message,
            BackgroundJob.finished_at: datetime.now().isoformat()
        }}
        job = await self.repository.update(job_id, query)
        return job

    async def error(self,
                    job_id: PydanticObjectId,
                    output_message: str
                    ) -> BackgroundJob:
        query = {"$set": {
            BackgroundJob.status: specs.JobStatuses.ERROR,
            BackgroundJob.output_message: output_message,
            BackgroundJob.finished_at: datetime.now().isoformat()
        }}
        job = await self.repository.update(job_id, query)
        return job

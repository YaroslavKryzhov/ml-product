from typing import List

from beanie import PydanticObjectId

from ml_api.apps.dataframes import specs, schemas
from ml_api.apps.dataframes.services.methods_service import \
    DataframeMethodsService
from ml_api.common.jobs_manager.base import JobsManager


class DataframeJobsManager(JobsManager):
    async def apply_changing_methods_async(
            self,
            dataframe_id: PydanticObjectId,
            method_params: List[schemas.ApplyMethodParams],
            new_filename: str):
        input_params = {
            "method_params": [param.dict() for param in method_params],
            "new_filename": new_filename
        }
        job = await self.job_service.start_apply_changing_methods(
            dataframe_id, input_params)
        try:
            await DataframeMethodsService(
                self._user_id).apply_changing_methods(
                dataframe_id, method_params, new_filename)
        except Exception as err:
            job_info = await self._process_error(err, job)
        else:
            job_info = await self.job_service.complete(job.id)
        self._publish_job(job_info)

    async def process_feature_importances_async(
            self,
            dataframe_id: PydanticObjectId,
            task_type: specs.FeatureSelectionTaskType,
            selection_params: List[schemas.SelectorMethodParams]):
        input_params = {
            "task_type": task_type.value,
            "selection_params": [param.dict() for param in selection_params]
        }
        job = await self.job_service.start_feature_importances(
            dataframe_id, input_params)
        try:
            await DataframeMethodsService(
                self._user_id).process_feature_importances(
                dataframe_id, task_type, selection_params)
        except Exception as err:
            job_info = await self._process_error(err, job)
        else:
            job_info = await self.job_service.complete(job.id)
        self.pubsub.publish_to_channel(job_info)

    async def copy_pipeline_async(self, dataframe_id_from, dataframe_id_to,
                                  new_filename):
        input_params = {
            "copy_from": str(dataframe_id_from),
            "new_filename": new_filename
        }
        job = await self.job_service.start_feature_importances(
            dataframe_id_to, input_params)
        try:
            await DataframeMethodsService(self._user_id).copy_pipeline(
                dataframe_id_from, dataframe_id_to, new_filename)
        except Exception as err:
            job_info = await self._process_error(err, job)
        else:
            job_info = await self.job_service.complete(job.id)
        self.pubsub.publish_to_channel(job_info)

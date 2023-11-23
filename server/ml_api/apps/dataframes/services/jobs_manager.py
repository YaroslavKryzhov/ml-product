from typing import List

from bunnet import PydanticObjectId
from starlette.responses import JSONResponse

from ml_api.apps.dataframes import specs, schemas
from ml_api.common.jobs_manager.base import JobsManager
from ml_api.common.celery_tasks.celery_tasks import apply_changing_methods, process_feature_importances


class DataframeJobsManager(JobsManager):
    def process_changing_methods_async(
            self,
            dataframe_id: PydanticObjectId,
            method_params: List[schemas.ApplyMethodParams],
            new_filename: str):
        input_params = {
            "method_params": method_params,
            "new_filename": new_filename
        }
        job = self.job_service.create_apply_changing_methods_job(
            dataframe_id, input_params)
        apply_changing_methods.delay(str(self._user_id), str(job.id))
        return JSONResponse(
            status_code=202,
            content={
                "message": "Задача принята и выполняется в фоновом режиме"}
        )

    def process_feature_importances_async(
            self,
            dataframe_id: PydanticObjectId,
            task_type: specs.FeatureSelectionTaskType,
            selection_params: List[schemas.SelectorMethodParams]):
        input_params = {
            "task_type": task_type.value,
            "selection_params": selection_params
        }
        job = self.job_service.create_feature_importances_job(
            dataframe_id, input_params)
        process_feature_importances.delay(str(self._user_id), str(job.id))
        return JSONResponse(
            status_code=202,
            content={
                "message": "Задача принята и выполняется в фоновом режиме"}
        )

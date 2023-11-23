from bunnet import PydanticObjectId
from fastapi.responses import JSONResponse

from ml_api.apps.ml_models.model import ModelMetadata
from ml_api.common.jobs_manager.base import JobsManager
from ml_api.common.celery_tasks.celery_tasks import process_model_training, \
    process_composition_training, process_prediction


class ModelJobsManager(JobsManager):
    def process_train_model_async(self, model_meta: ModelMetadata):
        input_params = {
            "model_name": model_meta.filename,
            "dataframe_id": model_meta.dataframe_id,
            "task_type": model_meta.task_type,
            "model_params": model_meta.model_params,
            "params_type": model_meta.params_type,
            "test_size": model_meta.test_size,
            "stratify": model_meta.stratify,
        }
        job = self.job_service.create_train_model_job(
            model_meta.id, input_params)
        process_model_training.delay(str(self._user_id), str(job.id))
        return JSONResponse(
            status_code=202,
            content={
                "message": "Задача принята и выполняется в фоновом режиме"}
        )

    def process_build_composition_async(self, composition_meta: ModelMetadata):
        input_params = {
            "composition_name": composition_meta.filename,
            "model_ids": composition_meta.composition_model_ids,
            "task_type": composition_meta.task_type,
            "composition_params": composition_meta.model_params,
        }
        job = self.job_service.create_train_model_job(
            composition_meta.id, input_params)
        process_composition_training.delay(str(self._user_id), str(job.id))
        return JSONResponse(
            status_code=202,
            content={
                "message": "Задача принята и выполняется в фоновом режиме"}
        )

    def predict_on_model_async(self,
                               dataframe_id: PydanticObjectId,
                               model_id: PydanticObjectId,
                               prediction_name: str,
                               apply_pipeline: bool):
        input_params = {
            "dataframe_id": dataframe_id,
            "model_id": model_id,
            "prediction_name": prediction_name,
            "apply_pipeline": apply_pipeline
        }
        job = self.job_service.create_train_model_job(
            model_id, input_params)
        process_prediction.delay(str(self._user_id), str(job.id))
        return JSONResponse(
            status_code=202,
            content={
                "message": "Задача принята и выполняется в фоновом режиме"}
        )

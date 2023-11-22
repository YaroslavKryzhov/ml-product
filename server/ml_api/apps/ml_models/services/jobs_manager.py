from beanie import PydanticObjectId
from fastapi import HTTPException

from ml_api.apps.ml_models.model import ModelMetadata
from ml_api.apps.ml_models.services.fit_predict_service import \
    ModelFitPredictService
from ml_api.common.jobs_manager.base import JobsManager


class ModelJobsManager(JobsManager):
    async def train_model_async(self, model_meta: ModelMetadata):
        input_params = {
            "model_name": model_meta.filename,
            "dataframe_id": model_meta.dataframe_id,
            "task_type": model_meta.task_type,
            "model_params": model_meta.model_params,
            "params_type": model_meta.params_type,
            "test_size": model_meta.test_size,
            "stratify": model_meta.stratify,
        }
        job = await self.job_service.start_train_model(
            model_meta.id, input_params)
        try:
            await ModelFitPredictService(
                self._user_id).train_model(model_meta=model_meta)
        except HTTPException as err:
            job_info = await self._process_http_exception(err, job)
        except Exception as err:
            job_info = await self._process_exception(err, job)
        else:
            job_info = await self.job_service.complete(job.id)
        self._publish_job(job_info)

    async def build_composition_async(self, composition_meta: ModelMetadata):
        input_params = {
            "composition_name": composition_meta.filename,
            "model_ids": composition_meta.composition_model_ids,
            "task_type": composition_meta.task_type,
            "composition_params": composition_meta.model_params,
        }
        job = await self.job_service.start_train_model(
            composition_meta.id, input_params)
        try:
            await ModelFitPredictService(
                self._user_id).train_composition(
                composition_meta=composition_meta)
        except HTTPException as err:
            job_info = await self._process_http_exception(err, job)
        except Exception as err:
            job_info = await self._process_exception(err, job)
        else:
            job_info = await self.job_service.complete(job.id)
        self._publish_job(job_info)

    async def predict_on_model_async(self,
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
        job = await self.job_service.start_train_model(
            model_id, input_params)
        try:
            await ModelFitPredictService(self._user_id).predict_on_model(
                source_df_id=dataframe_id,
                model_id=model_id,
                prediction_name=prediction_name,
                apply_pipeline=apply_pipeline)
        except HTTPException as err:
            job_info = await self._process_http_exception(err, job)
        except Exception as err:
            job_info = await self._process_exception(err, job)
        else:
            job_info = await self.job_service.complete(job.id)
        self._publish_job(job_info)


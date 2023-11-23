from fastapi import HTTPException

from ml_api.apps.dataframes.services.methods_service import \
    DataframeMethodsService
from ml_api.apps.jobs.services import BackgroundJobsService
from ml_api.apps.ml_models.services.fit_predict_service import \
    ModelFitPredictService
from ml_api.common.pubsub.client import get_pubsub_client
from ml_api.celery_worker import app_celery
from ml_api.apps.dataframes import schemas, specs


def _process_http_exception(err: HTTPException):
    error_type = type(err).__name__
    error_description = str(err.detail)
    message = f"{error_type}: {error_description}"
    return message


def _process_exception(err: Exception):
    error_type = type(err).__name__
    error_description = str(err)
    message = f"{error_type}: {error_description}"
    return message


@app_celery.task(name="apply_changing_methods", bind=True)
def apply_changing_methods(self, user_id: str, job_id: str):
    job_service = BackgroundJobsService(user_id)
    job = job_service.run_job(job_id)
    try:
        dataframe_id = job.object_id
        new_filename = job.input_params["new_filename"]
        methods_params = [schemas.ApplyMethodParams(**p) for p
                            in job.input_params["method_params"]]
        DataframeMethodsService(user_id)._process_changing_methods(
                dataframe_id, methods_params, new_filename)
    except HTTPException as err:
        message = _process_http_exception(err)
        job_info = job_service.error_job(job.id, message)
    except Exception as err:
        message = _process_exception(err)
        job_info = job_service.error_job(job.id, message)
    else:
        job_info = job_service.complete_job(job.id)
    pubsub = get_pubsub_client()
    pubsub.publish_to_channel(job_info)


@app_celery.task(name="process_feature_importances", bind=True)
def process_feature_importances(self, user_id: str, job_id: str):
    job_service = BackgroundJobsService(user_id)
    job = job_service.run_job(job_id)
    try:
        dataframe_id = job.object_id
        task_type = specs.FeatureSelectionTaskType(job.input_params["task_type"])
        selection_params = [schemas.SelectorMethodParams(**p) for p
                        in job.input_params["selection_params"]]
        DataframeMethodsService(user_id)._process_feature_importances(
                dataframe_id, task_type, selection_params)
    except HTTPException as err:
        message = _process_http_exception(err)
        job_info = job_service.error_job(job.id, message)
    except Exception as err:
        message = _process_exception(err)
        job_info = job_service.error_job(job.id, message)
    else:
        job_info = job_service.complete_job(job.id)
    pubsub = get_pubsub_client()
    pubsub.publish_to_channel(job_info)


@app_celery.task(name="process_model_training", bind=True)
def process_model_training(self, user_id: str, job_id: str):
    job_service = BackgroundJobsService(user_id)
    job = job_service.run_job(job_id)
    try:
        model_id = job.object_id
        ModelFitPredictService(user_id).train_model(model_id)
    except HTTPException as err:
        message = _process_http_exception(err)
        job_info = job_service.error_job(job.id, message)
    except Exception as err:
        message = _process_exception(err)
        job_info = job_service.error_job(job.id, message)
    else:
        job_info = job_service.complete_job(job.id)
    pubsub = get_pubsub_client()
    pubsub.publish_to_channel(job_info)


@app_celery.task(name="process_composition_training", bind=True)
def process_composition_training(self, user_id: str, job_id: str):
    job_service = BackgroundJobsService(user_id)
    job = job_service.run_job(job_id)
    try:
        composition_id = job.object_id
        ModelFitPredictService(user_id).train_composition(composition_id)
    except HTTPException as err:
        message = _process_http_exception(err)
        job_info = job_service.error_job(job.id, message)
    except Exception as err:
        message = _process_exception(err)
        job_info = job_service.error_job(job.id, message)
    else:
        job_info = job_service.complete_job(job.id)
    pubsub = get_pubsub_client()
    pubsub.publish_to_channel(job_info)


@app_celery.task(name="process_prediction", bind=True)
def process_prediction(self, user_id: str, job_id: str):
    job_service = BackgroundJobsService(user_id)
    job = job_service.run_job(job_id)
    try:
        model_id = job.object_id
        dataframe_id = job.input_params["dataframe_id"]
        prediction_name = job.input_params["prediction_name"]
        apply_pipeline = job.input_params["apply_pipeline"]
        ModelFitPredictService(user_id).predict_on_model(
            dataframe_id, model_id, prediction_name, apply_pipeline
        )
    except HTTPException as err:
        message = _process_http_exception(err)
        job_info = job_service.error_job(job.id, message)
    except Exception as err:
        message = _process_exception(err)
        job_info = job_service.error_job(job.id, message)
    else:
        job_info = job_service.complete_job(job.id)
    pubsub = get_pubsub_client()
    pubsub.publish_to_channel(job_info)

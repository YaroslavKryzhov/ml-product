import logging
from celery import Celery, Task

import ml_api.config as config
from ml_api.apps.dataframes.service.services import DataframeManagerService
from ml_api.common.db.session import Session
from ml_api.common.pubsub.client import PubSub

pub_sub = PubSub(config.CENTRIFUGO_PUB_API, config.CENTRIFUDO_API_KEY)

logger = logging.getLogger(__name__)

app_celery = Celery(
    "celery_ml_app",
    broker=config.BROKER_URI,
    backend=config.BACKEND_URI,
)


class BackgroundTask(Task):
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if status == "SUCCESS":
            pub_sub.publish_to_channel(message=f"SOME MESSAGE {str(task_id)}")
        else:
            pub_sub.publish_to_channel(message=f"OTHER MESSAGE {str(task_id)}")


@app_celery.task(name="apply_function")
def apply_function_celery(user_id: str, dataframe_id: str, function_name: str, params):
    try:
        with Session() as db:
            DataframeManagerService(db, user_id).apply_function(dataframe_id, function_name, params)
    except ConnectionError as e:
        logger.error(e)
    finally:
        db.close()
    return True


@app_celery.task(name="copy_pipeline")
def copy_pipeline_celery(user_id: str, dataframe_id_from: str, dataframe_id_to: str):
    try:
        with Session() as db:
            DataframeManagerService(db, user_id).copy_pipeline(dataframe_id_from, dataframe_id_to)
    except ConnectionError as e:
        logger.error(e)
    finally:
        db.close()
    return True


@app_celery.task(name="train_model")
def train_model_celery(db, user, dataframe_id: str, function_name: str, params):
    try:
        # pub_sub_client = Depends(pub_sub.get_pubsub_client)
        ModelsService(db, user).train_model(params)
    except ConnectionError as e:
        logger.error(e)
    finally:
        db.close()
    return True

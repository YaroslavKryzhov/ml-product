import logging
from celery import Task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import ml_api.config as config
from ml_api.apps.dataframes.services import DataframeManagerService
from ml_api.common.pubsub.client import PubSub
from ml_api.config import DATABASE_URL
from ml_api.celery_worker import app_celery

pub_sub = PubSub(config.CENTRIFUGO_PUB_API, config.CENTRIFUDO_API_KEY)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


logger = logging.getLogger(__name__)


class BackgroundTask(Task):
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pub_sub.publish_to_channel(user_id=self.user_id, task_id=task_id,
                                   status=status, message=retval)


@app_celery.task(base=BackgroundTask, name="apply_function", bind=True)
def apply_function_celery(self, user_id: str, dataframe_id: str, function_name: str, params):
    self.user_id = user_id
    try:
        with Session() as db:
            DataframeManagerService(db, user_id).apply_function(dataframe_id, function_name, params)
    except ConnectionError as e:
        logger.error(e)
        raise Exception("Can't connect to database")
    return True


@app_celery.task(base=BackgroundTask, name="copy_pipeline", bind=True)
def copy_pipeline_celery(self, user_id: str, dataframe_id_from: str, dataframe_id_to: str):
    self.user_id = user_id
    try:
        with Session() as db:
            DataframeManagerService(db, user_id).copy_pipeline(dataframe_id_from, dataframe_id_to)
    except ConnectionError as e:
        logger.error(e)
        raise Exception("Can't connect to database")
    return True


# @app_celery.task(name="train_model")
# def train_model_celery(db, user, dataframe_id: str, function_name: str, params):
#     try:
#         # pub_sub_client = Depends(pub_sub.get_pubsub_client)
#         ModelsService(db, user).train_model(params)
#     except ConnectionError as e:
#         logger.error(e)
#     finally:
#         db.close()
#     return True

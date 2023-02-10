import os
from api.source.apps.pipelines.service import PipelineService
from celery import Celery
from ml_api.common.db.session import SessionLocal
from fastapi import Depends
from ml_api.common.dependencies import pub_sub
import logging


logger = logging.getLogger(__name__)


celery_queue = Celery(__name__)
celery_queue.conf["BROKER_URL"] = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
celery_queue.conf["CELERY_RESULT_BACKEND"] = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")


@celery_queue.task(name="create_task")
def create_task(pipeline_in: int):
    try:
        db = SessionLocal()
        logger.info('Create session & celery task started')
        # pub_sub_client = Depends(pub_sub.get_pubsub_client)
        PipelineService(db=db).run(pipeline_in)

    except ConnectionError as e:
        logger.error(e)
    finally:
        db.close()

    return True

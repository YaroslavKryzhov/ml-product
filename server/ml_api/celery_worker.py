from celery import Celery

import ml_api.config as config


app_celery = Celery(
    "celery_ml_app",
    broker=config.BROKER_URI,
    backend=config.BACKEND_URI,
    include=["ml_api.common.celery_tasks.celery_tasks"],
)

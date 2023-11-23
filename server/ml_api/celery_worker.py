from celery import Celery
from celery.signals import worker_process_init
from bunnet import init_bunnet
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from ml_api import config
from ml_api.apps.users.model import User
from ml_api.apps.dataframes.model import DataFrameMetadata
from ml_api.apps.ml_models.model import ModelMetadata
from ml_api.apps.training_reports.model import Report
from ml_api.apps.jobs.model import BackgroundJob

app_celery = Celery(
    "celery_ml_app",
    broker=config.BROKER_URI,
    backend=config.BACKEND_URI,
    include=["ml_api.common.celery_tasks.celery_tasks"],
)


@worker_process_init.connect
def on_worker_init(*args, **kwargs):
    db = MongoClient(config.MONGO_DATABASE_URI)[config.MONGO_DB_NAME]
    try:
        init_bunnet(db,
            document_models=[User, DataFrameMetadata, ModelMetadata, Report,
                             BackgroundJob])
    except ServerSelectionTimeoutError as sste:
        print(sste)
    print("Bunnet initialized")

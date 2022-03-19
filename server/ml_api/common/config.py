from ml_api.common.mongo_config import DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT, DATABASE_HOST

PROJECT_NAME = 'ML Project'
VERSION = '0.0.1'

DEFAULT_DB_NAME = 'ml_project_mongo'
DATABASE_URL = f"mongodb://{DATABASE_USER}:{DATABASE_PASSWORD}@" \
                                 f"{DATABASE_HOST}:{DATABASE_PORT}/{DEFAULT_DB_NAME}"

ALLOW_ORIGINS = ['*']
from typing import Generator

from ml_api.common.database.mongo_manager import MongoDBConnectionManager
from ml_api.common.config import DATABASE_URL, DEFAULT_DB_NAME


def get_db() -> Generator:
    with MongoDBConnectionManager(connection_string=DATABASE_URL, database=DEFAULT_DB_NAME) as db:
        yield db

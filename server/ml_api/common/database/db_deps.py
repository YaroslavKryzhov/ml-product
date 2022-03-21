from typing import Generator

from ml_api.common.database.db_session_manager import DBConnectionManager
from ml_api.common.config import DATABASE_URL


def get_db() -> Generator:
    with DBConnectionManager(connection_string=DATABASE_URL) as db:
        yield db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnectionManager:

    def __init__(self, connection_string: str):
        self._engine = create_engine(connection_string, pool_pre_ping=True)
        self._Session = sessionmaker(bind=self._engine, autocommit=False, autoflush=False)

    def __enter__(self):
        self._db = self._Session()
        return self._db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db.close()

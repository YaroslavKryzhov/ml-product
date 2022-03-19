from pymongo import MongoClient


class MongoDBConnectionManager:

    def __init__(self, connection_string: str, database):
        self.connection_string = connection_string
        self.database = database
        self._client = None

    def __enter__(self):
        self._client = MongoClient(self.connection_string)
        self._db = self._client[self.database]
        return self._db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._client.close()

from ml_api.apps.csv.models import Csv

class CsvCRUD:

    def __init__(self, db):
        self._db = db

    # CREATE
    def load_csv(self) -> bool:
        pass

    # READ
    def read_csv(self) -> Csv:
        pass

    # UPDATE
    def update_csv(self) -> Csv:
        pass

    # DELETE
    def delete_csv(self) -> bool:
        pass
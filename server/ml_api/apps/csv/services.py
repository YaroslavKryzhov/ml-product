from ml_api.apps.csv.models import Csv
from ml_api.apps.csv.repository import CsvCRUD


class CsvService:

    def __init__(self, db):
        self._db = db

    def load_csv_to_db(self):
        CsvCRUD(self._db).load_csv()
        pass

    def read_csv_from_db(self) -> Csv:
        csv = CsvCRUD(self._db).read_csv()
        return csv

    def fill_spaces(self):
        pass

    def remove_duplicates(self):
        pass

    def remove_outlayers(self):
        pass

    def standartize_features(self):
        pass

    def normalize_features(self):
        pass

    def train_test_split(self):
        pass
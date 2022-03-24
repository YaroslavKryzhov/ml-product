import pandas as pd

from ml_api.apps.csv.models import Csv
from ml_api.apps.csv.repository import CsvFileCRUD, CsvPostgreCRUD


class CsvService:

    def __init__(self, db, user):
        self._db = db
        self._user = user

    def upload_csv_to_db(self, file, filename: str):
        CsvFileCRUD(self._user).upload_csv(filename, file)
        # CsvPostgreCRUD(self._db).new_csv(filename)
        pass

    def download_csv_from_db(self, filename: str):
        file = CsvFileCRUD(self._user).download_csv(filename)
        return file

    def read_csv_from_db(self, filename: str) -> pd.DataFrame:
        df = CsvFileCRUD(self._user).read_csv(filename)
        return df.head(10)

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
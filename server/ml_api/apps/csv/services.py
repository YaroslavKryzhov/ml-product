import pandas as pd

from ml_api.apps.csv.models import Csv
from ml_api.apps.csv.repository import CsvFileCRUD, CsvPostgreCRUD
from fastapi import UploadFile


class CsvService:

    def __init__(self, db):
        self._db = db

    def upload_csv_to_db(self, file, filename: str):
        CsvFileCRUD().upload_csv(filename, file)
        CsvPostgreCRUD(self._db).new_csv(filename)
        pass

    def read_csv_from_db(self, filename: str) -> pd.DataFrame:
        df = CsvFileCRUD().read_csv(filename)
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
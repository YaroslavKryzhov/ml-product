import os
import shutil
from typing import List

import pandas as pd
from sqlalchemy.orm import Session


from ml_api.apps.csv.models import Csv


class CsvPostgreCRUD:

    def __init__(self, session: Session):
        self.session = session

    # CREATE
    def new_csv(self, filename: str):
        new_obj = Csv(name=filename)
        self.session.add(new_obj)
        self.session.commit()

    # READ
    def read_csv(self) -> List[Csv]:
        return self.session.query(Csv).all()

    # UPDATE
    def update_csv(self) -> Csv:
        pass

    # DELETE
    def delete_csv(self) -> bool:
        pass


class CsvFileCRUD:

    def __init__(self, user: str = 'admin'):
        self.csv_path = f'ml_data/{user}/csv/'

    # CREATE
    def upload_csv(self, filename: str, file):
        print(os.path.join(self.csv_path, filename))
        with open(filename, 'wb') as buffer:
            shutil.copyfileobj(file, buffer)

    # READ
    def read_csv(self, filename: str) -> pd.DataFrame:
        data = pd.read_csv(filename)
        return data

    def download_csv(self, filename: str):
        """ function for csv-file download """
        pass

    # UPDATE
    def update_csv(self, filename: str, data: pd.DataFrame):
        data.to_csv(os.path.join(self.csv_path, filename))

    # DELETE
    def delete_csv(self, filename: str):
        os.remove(os.path.join(self.csv_path, filename))

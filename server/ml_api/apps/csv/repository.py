import os
import shutil
from typing import List

import pandas as pd
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from ml_api.common.config import ROOT_DIR
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

    def __init__(self, user: str):
        self.user_path = os.path.join(ROOT_DIR, user)
        if not os.path.exists(self.user_path):
            os.makedirs(self.user_path)

    # CREATE
    def upload_csv(self, filename: str, file):
        csv_path = os.path.join(self.user_path, filename)
        print(csv_path)
        with open(csv_path, 'wb') as buffer:
            shutil.copyfileobj(file, buffer)

    # READ
    def read_csv(self, filename: str) -> pd.DataFrame:
        csv_path = os.path.join(self.user_path, filename)
        data = pd.read_csv(csv_path)
        return data

    def download_csv(self, filename: str):
        csv_path = os.path.join(self.user_path, filename)
        return FileResponse(path=csv_path)

    # UPDATE
    def update_csv(self, filename: str, data: pd.DataFrame):
        data.to_csv(os.path.join(self.csv_path, filename))

    # DELETE
    def delete_csv(self, filename: str):
        os.remove(os.path.join(self.csv_path, filename))

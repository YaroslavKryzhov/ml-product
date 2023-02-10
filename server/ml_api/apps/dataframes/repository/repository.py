from typing import Dict, List
from datetime import datetime
from uuid import UUID

import pandas as pd
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from ml_api.common.file_manager.base import FileCRUD
from ml_api.apps.dataframes.repository.models import DataFrame
from ml_api.apps.dataframes.controller.schemas import DataFrameInfo


class DataFrameInfoCRUD:
    def __init__(self, session: Session, user):
        self.session = session
        self.user_id = str(user.id)

    def get(self, dataframe_id: UUID) -> DataFrameInfo:
        dataframe = (
            self.session.query(DataFrame).filter(DataFrame.id == dataframe_id)
            .first()
        )
        if dataframe:
            return DataFrameInfo.from_orm(dataframe)
        return None

    def get_by_name(self, filename: str) -> DataFrameInfo:
        dataframe = (
            self.session.query(DataFrame).filter(DataFrame.filename == filename)
            .first()
        )
        if dataframe:
            return DataFrameInfo.from_orm(dataframe)
        return None

    def get_all(self) -> List[DataFrameInfo]:
        documents = (
            self.session.query(DataFrame)
            .filter(DataFrame.user_id == self.user_id)
            .all()
        )
        result = []
        for document in documents:
            result.append(DataFrameInfo.from_orm(document))
        return result

    def create(self, filename: str) -> DataFrame:
        new_obj = DataFrame(
            filename=filename,
            user_id=self.user_id,
            created_at=str(datetime.now()),
            updated_at=str(datetime.now()),
            pipeline=[],
            column_types=None,
        )
        self.session.add(new_obj)
        self.session.commit()
        self.session.refresh(new_obj)
        return DataFrameInfo.from_orm(new_obj)

    # UPDATE
    def update(self, dataframe_id: UUID, query: Dict):
        self.session.query(DataFrame).filter(DataFrame.id == dataframe_id
                                             ).update(query)
        self.session.commit()

    # DELETE
    def delete(self, dataframe_id: UUID):
        self.session.query(DataFrame).filter(DataFrame.id == dataframe_id
                                             ).delete()
        self.session.commit()


class DataFrameFileCRUD(FileCRUD):

    def read_csv(self, file_uuid: str) -> pd.DataFrame:
        csv_path = self._get_path(file_uuid)
        data = pd.read_csv(csv_path)
        return data

    def download_csv(self, file_uuid: str) -> FileResponse:
        file_response = self.download(file_uuid=file_uuid)
        file_response.media_type = 'text/csv'
        return file_response

    def save_csv(self, file_uuid: str, data: pd.DataFrame):
        data.to_csv(self._get_path(file_uuid), index=False)

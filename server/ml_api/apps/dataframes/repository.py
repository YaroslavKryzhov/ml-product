from typing import Dict, List
from datetime import datetime
from uuid import UUID

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import exc as sql_exceptions
from fastapi.responses import FileResponse
from fastapi import HTTPException, status

from ml_api.common.file_manager.base import FileCRUD
from ml_api.apps.dataframes.models import DataFrame
from ml_api.apps.dataframes.schemas import DataFrameInfo


class DataFrameInfoCRUD:
    def __init__(self, session: Session, user_id: str):
        self.session = session
        self.user_id = user_id

    def get(self, dataframe_id: UUID) -> DataFrameInfo:
        dataframe = (
            self.session.query(DataFrame).filter(DataFrame.id == dataframe_id)
            .first()
        )
        if dataframe is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dataframe with id {dataframe_id} not found."
            )
        return DataFrameInfo.from_orm(dataframe)

    def get_all(self) -> List[DataFrameInfo]:
        dataframes = (
            self.session.query(DataFrame)
            .filter(DataFrame.user_id == self.user_id)
            .all()
        )
        result = []
        for dataframe in dataframes:
            result.append(DataFrameInfo.from_orm(dataframe))
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
        try:
            self.session.commit()
        except sql_exceptions.IntegrityError as err:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(err)
            )
        except sql_exceptions.SQLAlchemyError as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )
        self.session.refresh(new_obj)
        return DataFrameInfo.from_orm(new_obj)

    # UPDATE
    def update(self, dataframe_id: UUID, query: Dict):
        try:
            res = self.session.query(DataFrame).filter(DataFrame.id == dataframe_id
                                                 ).update(query)
            if res == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Dataframe with id {dataframe_id} not found."
                )
        except sql_exceptions.IntegrityError as err:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(err)
            )
        except sql_exceptions.SQLAlchemyError as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )
        self.session.commit()

    # DELETE
    def delete(self, dataframe_id: UUID):
        res = self.session.query(DataFrame).filter(DataFrame.id == dataframe_id
                                             ).delete()
        if res == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dataframe with id {dataframe_id} not found."
            )
        self.session.commit()


class DataFrameFileCRUD(FileCRUD):

    def read_csv(self, file_uuid: UUID) -> pd.DataFrame:
        csv_path = self._get_path(file_uuid)
        try:
            data = pd.read_csv(csv_path)
        except FileNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Dataframe with id {file_uuid} not found."
            )
        return data

    def download_csv(self, file_uuid: UUID, filename: str) -> FileResponse:
        file_response = self.download(file_uuid=file_uuid, filename=filename)
        file_response.media_type = 'text/csv'
        return file_response

    def save_csv(self, file_uuid: UUID, data: pd.DataFrame):
        data.to_csv(self._get_path(file_uuid), index=False)

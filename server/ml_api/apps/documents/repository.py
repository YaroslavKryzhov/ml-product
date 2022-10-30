import os
import shutil
from typing import Dict, List
from datetime import datetime
from uuid import UUID

import pandas as pd
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from ml_api.common.config import ROOT_DIR
from ml_api.apps.documents.models import Document
from ml_api.apps.documents.schemas import DocumentShortInfo, DocumentFullInfo


class BaseCRUD:
    def __init__(self, user):
        self.user_id = str(user.id)
        self.user_path = os.path.join(ROOT_DIR, self.user_id, 'documents')
        if not os.path.exists(self.user_path):
            os.makedirs(self.user_path)

    def _file_path(self, filename) -> str:
        return os.path.join(self.user_path, filename)


class DocumentPostgreCRUD(BaseCRUD):
    def __init__(self, session: Session, user):
        super().__init__(user)
        self.session = session

    # CREATE
    def create(self, filename: str):
        new_obj = Document(
            name=filename,
            filepath=self._file_path(filename),
            user_id=self.user_id,
            upload_date=str(datetime.now()),
            change_date=str(datetime.now()),
            pipeline=[],
            column_types=None,
        )
        self.session.add(new_obj)
        self.session.commit()

    # READ
    def read_by_uuid(self, uuid: UUID) -> str:
        name = (
            self.session.query(Document.name)
            .filter(Document.id == uuid)
            .first()[0]
        )
        return name

    def read_by_name(self, filename: str) -> DocumentFullInfo:
        filepath = self._file_path(filename)
        document = (
            self.session.query(
                Document.id,
                Document.name,
                Document.upload_date,
                Document.change_date,
                Document.column_types,
                Document.pipeline,
            )
            .filter(Document.filepath == filepath)
            .first()
        )
        if document:
            return DocumentFullInfo.from_orm(document)
        return None

    def read_all(self) -> List[DocumentShortInfo]:
        documents = (
            self.session.query(
                Document.name,
                Document.upload_date,
                Document.change_date,
                Document.pipeline,
            )
            .filter(Document.user_id == self.user_id)
            .all()
        )
        result = []
        for document in documents:
            result.append(DocumentShortInfo.from_orm(document))
        return result

    # UPDATE
    def update(self, filename: str, query: Dict):
        filepath = self._file_path(filename)
        if query.get('name', None):
            query['filepath'] = self._file_path(query['name'])
        self.session.query(Document).filter(
            Document.filepath == filepath
        ).update(query)
        self.session.commit()

    # DELETE
    def delete(self, filename: str):
        # sqlalchemy.exc.IntegrityError:
        filepath = self._file_path(filename)
        self.session.query(Document).filter(
            Document.filepath == filepath
        ).delete()
        self.session.commit()


class DocumentFileCRUD(BaseCRUD):

    # CREATE
    def create(self, filename: str, file):
        csv_path = self._file_path(filename)
        with open(csv_path, 'wb') as buffer:
            shutil.copyfileobj(file, buffer)

    # READ
    def read_df(self, filename: str) -> pd.DataFrame:
        """DEV USE: Read CSV and return DataFrame object"""
        csv_path = self._file_path(filename)
        data = pd.read_csv(csv_path)
        return data

    def download(self, filename: str) -> FileResponse:
        csv_path = self._file_path(filename)
        return FileResponse(
            path=csv_path, filename=filename, media_type='text/csv'
        )

    # UPDATE
    def update(self, filename: str, data: pd.DataFrame):
        """DEV USE: Save DataFrame object in CSV format"""
        data.to_csv(os.path.join(self.user_path, filename), index=False)

    def rename(self, filename: str, new_filename: str):
        old_path = self._file_path(filename)
        new_path = self._file_path(new_filename)
        shutil.move(old_path, new_path)

    # DELETE
    def delete(self, filename: str):
        os.remove(self._file_path(filename))

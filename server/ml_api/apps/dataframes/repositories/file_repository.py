import tempfile
from pathlib import Path

import pandas as pd
from fastapi.responses import FileResponse
from beanie import PydanticObjectId

from ml_api.common.file_manager.base import FileCRUD
from ml_api.config import ROOT_DIR
from ml_api.apps.dataframes import errors


class DataFrameFileCRUD(FileCRUD):
    def __init__(self, user_id):
        self.user_id = user_id

    def _get_csv_path(self, file_id: PydanticObjectId):
        user_path = Path(ROOT_DIR) / str(self.user_id) / "dataframes"
        user_path.mkdir(parents=True, exist_ok=True)
        return user_path / f"{file_id}.csv"

    def upload_csv(self, file_id: PydanticObjectId,
                   file: tempfile.SpooledTemporaryFile) -> FileResponse:
        csv_path = self._get_csv_path(file_id)
        self._upload(csv_path, file)

    def download_csv(self, file_id: PydanticObjectId, filename: str
                     ) -> FileResponse:
        csv_path = self._get_csv_path(file_id)
        if not filename.endswith('.csv'):
            filename += '.csv'
        file_response = self._download(path=csv_path, filename=filename)
        file_response.media_type = "text/csv"
        return file_response

    def read_csv(self, file_id: PydanticObjectId) -> pd.DataFrame:
        csv_path = self._get_csv_path(file_id)
        try:
            data = pd.read_csv(csv_path)
        except FileNotFoundError:
            raise errors.DataFrameFileNotFoundError(file_id)
        return data

    def save_csv(self, file_id: PydanticObjectId, data: pd.DataFrame):
        csv_path = self._get_csv_path(file_id)
        data.to_csv(csv_path, index=False)

    def delete_csv(self, file_id: PydanticObjectId):
        csv_path = self._get_csv_path(file_id)
        self._delete(csv_path)

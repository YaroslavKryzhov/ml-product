import tempfile
import os
from uuid import UUID

from fastapi.responses import FileResponse
from fastapi import HTTPException, status

import ml_api.config as config


class FileCRUD:
    def __init__(self, user_id):
        self.user_id = user_id

    def _get_path(self, file_id: UUID):
        user_path = os.path.join(config.ROOT_DIR, str(self.user_id))
        if not os.path.exists(user_path):
            os.makedirs(user_path)
        return os.path.join(user_path, str(file_id))

    def upload(self, file_id: UUID, file: tempfile.SpooledTemporaryFile) -> str:
        path = self._get_path(file_id)
        context = file.read()
        with open(path, 'wb') as f:
            f.write(context)
        return file_id

    def download(self, file_id: UUID, filename: str) -> FileResponse:
        path = self._get_path(file_id)
        return FileResponse(path=path, filename=filename)

    def replace(self, file_id: UUID, file: tempfile.SpooledTemporaryFile) -> str:
        path = self._get_path(file_id)
        context = file.read()
        with open(path, 'wb') as f:
            f.write(context)
        return file_id

    def delete(self, file_id: UUID):
        try:
            os.remove(self._get_path(file_id))
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

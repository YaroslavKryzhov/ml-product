import tempfile
import os
from uuid import UUID

from fastapi.responses import FileResponse
from fastapi import HTTPException, status

import ml_api.config as config


class FileCRUD:

    @staticmethod
    def _get_path(file_uuid: UUID):
        return os.path.join(config.ROOT_DIR, str(file_uuid))

    def upload(self, file_uuid: UUID, file: tempfile.SpooledTemporaryFile) -> str:
        path = self._get_path(file_uuid)
        context = file.read()
        with open(path, 'wb') as f:
            f.write(context)
        return file_uuid

    def download(self, file_uuid: UUID, filename: str) -> FileResponse:
        path = self._get_path(file_uuid)
        return FileResponse(path=path, filename=filename)

    def replace(self, file_uuid: UUID, file: tempfile.SpooledTemporaryFile) -> str:
        path = self._get_path(file_uuid)
        context = file.read()
        with open(path, 'wb') as f:
            f.write(context)
        return file_uuid

    def delete(self, file_uuid: UUID):
        try:
            os.remove(self._get_path(file_uuid))
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err)
            )

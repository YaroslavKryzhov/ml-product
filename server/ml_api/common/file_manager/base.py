import tempfile
from pathlib import Path

from beanie import PydanticObjectId

from fastapi.responses import FileResponse
from fastapi import HTTPException, status

import ml_api.config as config


class FileCRUD:
    def __init__(self, user_id):
        self.user_id = user_id

    def _get_path(self, file_id: PydanticObjectId):
        user_path = Path(config.ROOT_DIR) / str(self.user_id)
        user_path.mkdir(parents=True, exist_ok=True)
        return user_path / str(file_id)

    def upload(self, file_id: PydanticObjectId, file: tempfile.SpooledTemporaryFile) -> str:
        path = self._get_path(file_id)
        context = file.read()
        path.write_bytes(context)

    def download(self, file_id: PydanticObjectId, filename: str) -> FileResponse:
        path = self._get_path(file_id)
        if path.exists():
            return FileResponse(path=path, filename=filename)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"File with ID {file_id} not found"
            )

    def delete(self, file_id: PydanticObjectId):
        path = self._get_path(file_id)
        if path.exists():
            path.unlink()
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"File with ID {file_id} not found"
            )

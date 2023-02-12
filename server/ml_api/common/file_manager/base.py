import tempfile
import os

from fastapi.responses import FileResponse

import ml_api.config as config


class FileCRUD:

    @staticmethod
    def _get_path(file_uuid):
        return os.path.join(config.ROOT_DIR, file_uuid)

    def upload(self, file_uuid: str, file: tempfile.SpooledTemporaryFile) -> str:
        path = self._get_path(file_uuid)
        context = file.read()
        with open(path, 'wb') as f:
            f.write(context)
        return file_uuid

    def download(self, file_uuid: str, filename: str) -> FileResponse:
        path = self._get_path(file_uuid)
        return FileResponse(path=path, filename=filename)

    def replace(self, file_uuid: str, file: tempfile.SpooledTemporaryFile) -> str:
        path = self._get_path(file_uuid)
        context = file.read()
        with open(path, 'wb') as f:
            f.write(context)
        return file_uuid

    def delete(self, file_uuid: str):
        os.remove(self._get_path(file_uuid))

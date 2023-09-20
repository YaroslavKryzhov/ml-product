import tempfile
from pathlib import Path

from fastapi.responses import FileResponse
from fastapi import HTTPException, status


class FileCRUD:

    def _upload(self, path: Path, file: tempfile.SpooledTemporaryFile) -> str:
        context = file.read()
        path.write_bytes(context)

    def _download(self, path: Path, filename: str) -> FileResponse:
        if path.exists():
            return FileResponse(path=path, filename=filename)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"File {path.name} not found"
            )

    def _delete(self, path: Path):
        if path.exists():
            path.unlink()
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"File {path.name} not found"
            )

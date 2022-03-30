from fastapi import APIRouter, Depends, UploadFile, File

from ml_api.common.database.db_deps import get_db
from ml_api.common.database.users_deps import get_current_user
from ml_api.apps.document.services import CsvService
from ml_api.apps.document.schemas import Csv


csv_router = APIRouter(
    prefix="/csv",
    tags=["csv"],
    responses={404: {"description": "Not found"}}
)


@csv_router.post("")
def load_csv(file: UploadFile = File(...), db: get_db = Depends(), user: str = Depends(get_current_user)):
    CsvService(db, user).upload_csv_to_db(file=file.file, filename=file.filename)
    return {"filename": file.filename}


@csv_router.get("")
def read_csv(filename: str, db: get_db = Depends(), user: str = Depends(get_current_user)):
    result = CsvService(db, user).read_csv_from_db(filename)
    return result.to_json()


@csv_router.get("/download")
def download_csv(filename: str, db: get_db = Depends(), user: str = Depends(get_current_user)):
    result = CsvService(db, user).download_csv_from_db(filename)
    return result

from fastapi import APIRouter, Depends, UploadFile, File

from ml_api.common.database.db_deps import get_db
from ml_api.apps.csv.services import CsvService
from ml_api.apps.csv.schemas import Csv


csv_router = APIRouter(
    prefix="/csv",
    tags=["csv"],
    responses={404: {"description": "Not found"}}
)


@csv_router.post("")
def load_csv(file: UploadFile = File(...), db: get_db = Depends()):
    CsvService(db).upload_csv_to_db(file=file.file, filename=file.filename)
    return {"filename": file.filename}


@csv_router.get("")
def read_csv(filename: str, db: get_db = Depends()):
    result = CsvService(db).read_csv_from_db(filename)
    return result.to_json()

from fastapi import APIRouter, Depends

from ml_api.common.database.db_deps import get_db
from ml_api.apps.csv.services import CsvService
from ml_api.apps.csv.schemas import Csv


csv_router = APIRouter(
    prefix="/csv",
    tags=["csv"],
    responses={404: {"description": "Not found"}}
)


@csv_router.get("", response_model=Csv)
def load_csv(csv_path: str, db: get_db = Depends()):
    result = CsvService(db).load_csv_to_db()
    return result


@csv_router.post("", response_model=Csv)
def read_csv(csv_path: str, db: get_db = Depends()):
    result = CsvService(db).read_csv_from_db()
    return result

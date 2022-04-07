from fastapi import APIRouter, Depends, UploadFile, File

from ml_api.common.database.db_deps import get_db
from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.schemas import UserDB
from ml_api.apps.documents.services import DocumentService
from ml_api.apps.documents.schemas import DocumentDB


documents_crud_router = APIRouter(
    prefix="/document",
    tags=["Document Utils"],
    responses={404: {"description": "Not found"}}
)


@documents_crud_router.post("")
def load_document(file: UploadFile = File(...), db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    DocumentService(db, user).upload_document_to_db(file=file.file, filename=file.filename)
    return {"filename": file.filename}


@documents_crud_router.get("")
def read_document(filename: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    result = DocumentService(db, user).read_document_from_db(filename)
    return result.to_json()


@documents_crud_router.get("/download")
def download_document(filename: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    result = DocumentService(db, user).download_document_from_db(filename)
    return result


@documents_crud_router.put("/rename")
def rename_document(filename: str, new_filename: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    DocumentService(db, user).rename_document(filename, new_filename)
    return {"filename": new_filename}


@documents_crud_router.delete("")
def delete_document(filename: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    DocumentService(db, user).delete_document_from_db(filename)
    return {"filename": filename}


documents_method_router = APIRouter(
    prefix="/document/process",
    tags=["Document Methods"],
    responses={404: {"description": "Not found"}}
)


@documents_method_router.put("/duplicates")
def remove_duplicates(filename: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    DocumentService(db, user).remove_duplicates(filename)
    return {"filename": filename}


@documents_method_router.put("/drop_na")
def remove_duplicates(filename: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    DocumentService(db, user).drop_na(filename)
    return {"filename": filename}


@documents_method_router.put("/HZR_outlier_interquartile_distance")
def outlier_interquartile_distance(filename: str, low_quantile: float, up_quantile: float, coef: float,\
        db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    DocumentService(db, user).outlier_interquartile_distance(filename, low_quantile, up_quantile, coef)
    return {"filename": filename}

  
@documents_method_router.put("/outlier_three_sigma")
def outlier_three_sigma(filename: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    DocumentService(db, user).outlier_three_sigma(filename)
    return {"filename": filename}

  
@documents_method_router.put("/miss_insert_mean_mode")
def miss_insert_mean_mode(filename: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    DocumentService(db, user).miss_insert_mean_mode(filename, threshold_unique=10) #Границу вводит юзер
    return {"filename": filename}


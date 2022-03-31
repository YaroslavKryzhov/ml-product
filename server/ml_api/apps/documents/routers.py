from fastapi import APIRouter, Depends, UploadFile, File

from ml_api.common.database.db_deps import get_db
from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.schemas import UserDB
from ml_api.apps.documents.services import DocumentService
from ml_api.apps.documents.schemas import DocumentDB


documents_router = APIRouter(
    prefix="/document",
    tags=["document"],
    responses={404: {"description": "Not found"}}
)


@documents_router.post("")
def load_document(file: UploadFile = File(...), db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    DocumentService(db, user).upload_document_to_db(file=file.file, filename=file.filename)
    return {"filename": file.filename}


@documents_router.get("")
def read_document(filename: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    result = DocumentService(db, user).read_document_from_db(filename)
    return result.to_json()


@documents_router.get("/download")
def download_document(filename: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    result = DocumentService(db, user).download_document_from_db(filename)
    return result


@documents_router.put("/rename")
def rename_document(filename: str, new_filename: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    DocumentService(db, user).rename_document(filename, new_filename)
    return {"filename": new_filename}


@documents_router.delete("")
def delete_document(filename: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    DocumentService(db, user).delete_document_from_db(filename)
    return {"filename": filename}

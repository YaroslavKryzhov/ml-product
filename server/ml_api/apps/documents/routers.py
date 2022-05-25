from typing import List, Dict

from fastapi import APIRouter, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse

from ml_api.common.database.db_deps import get_db
from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.models import User
from ml_api.apps.documents.services import DocumentService
from ml_api.apps.documents.schemas import DocumentFullInfo, DocumentShortInfo, ColumnMarks, AvailableFunctions, \
    ServiceResponse, ReadDocumentResponse, TaskType, ColumnDescription

documents_file_router = APIRouter(
    prefix="/document",
    tags=["Document As File"],
    responses={404: {"description": "Not found"}}
)


@documents_file_router.post("", response_model=ServiceResponse)
def upload_document(filename: str, file: UploadFile = File(...), db: get_db = Depends(),
                    user: User = Depends(current_active_user)):
    result = DocumentService(db, user).upload_document_to_db(file=file.file, filename=filename)
    if result:
        return ServiceResponse(status_code=status.HTTP_200_OK, content=f"The document '{filename}' successfully added")
    else:
        return ServiceResponse(status_code=status.HTTP_409_CONFLICT, content=f"The document name '{filename}'"
                                                                             f" is already taken")


@documents_file_router.get("/download")
def download_document(filename: str, db: get_db = Depends(), user: User = Depends(current_active_user)):
    result = DocumentService(db, user).download_document_from_db(filename)
    return result


@documents_file_router.put("/rename", response_model=ServiceResponse)
def rename_document(filename: str, new_filename: str, db: get_db = Depends(),
                    user: User = Depends(current_active_user)):
    result = DocumentService(db, user).rename_document(filename, new_filename)
    if result:
        return ServiceResponse(status_code=status.HTTP_200_OK, content=f"The document '{filename}' successfully renamed"
                                                                       f"to '{new_filename}'")
    else:
        return ServiceResponse(status_code=status.HTTP_409_CONFLICT, content=f"The document name '{new_filename}'"
                                                                             f" is already taken")


@documents_file_router.delete("", response_model=ServiceResponse)
def delete_document(filename: str, db: get_db = Depends(), user: User = Depends(current_active_user)):
    result = DocumentService(db, user).delete_document_from_db(filename)
    if result:
        return ServiceResponse(status_code=status.HTTP_200_OK, content=f"The document '{filename}' "
                                                                       f"successfully deleted")
    else:
        return ServiceResponse(status_code=status.HTTP_409_CONFLICT, content=f"The document '{filename}'"
                                                                             f" is is used in some model!")


@documents_file_router.get("/all", response_model=List[DocumentShortInfo])
def read_all_user_documents(db: get_db = Depends(), user: User = Depends(current_active_user)):
    result = DocumentService(db, user).read_all_documents_info()
    return result


@documents_file_router.get("/info", response_model=DocumentFullInfo)
def read_document_info(filename: str, db: get_db = Depends(), user: User = Depends(current_active_user)):
    result = DocumentService(db, user).read_document_info(filename=filename)
    return result


documents_df_router = APIRouter(
    prefix="/document/df",
    tags=["Document As DataFrame"],
    responses={404: {"description": "Not found"}}
)


@documents_df_router.get("", response_model=ReadDocumentResponse)
def read_document_with_pagination(filename: str, page: int = 1, db: get_db = Depends(),
                                  user: User = Depends(current_active_user)):
    result = DocumentService(db, user).read_document_with_pagination(filename, page)
    return result


@documents_df_router.get("/stats/info", response_model=Dict[str, Dict])
def document_stat_info(filename: str, db: get_db = Depends(), user: User = Depends(current_active_user)):
    result = DocumentService(db, user).get_document_stat_info(filename)
    return result


@documents_df_router.get("/stats/describe", response_model=Dict[str, Dict])
def document_stat_describe(filename: str, db: get_db = Depends(), user: User = Depends(current_active_user)):
    result = DocumentService(db, user).get_document_stat_description(filename)
    return result


@documents_df_router.get("/columns", response_model=List)
def get_column_names(filename: str, db: get_db = Depends(), user: User = Depends(current_active_user)):
    result = DocumentService(db, user).read_document_columns(filename)
    return result


@documents_df_router.get("/stats/columns", response_model=List[ColumnDescription])
def column_stat_description(filename: str, db: get_db = Depends(), user: User = Depends(current_active_user)):
    result = DocumentService(db, user).get_column_stat_description(filename)
    return result


documents_method_router = APIRouter(
    prefix="/document/process",
    tags=["Document Methods"],
    responses={404: {"description": "Not found"}}
)


@documents_method_router.put("/target", response_model=ServiceResponse)
def set_target_feature(filename: str, target_column: str, task_type: TaskType, db: get_db = Depends(),
                       user: User = Depends(current_active_user)):
    DocumentService(db, user).set_column_marks(filename, target_column, task_type)
    return ServiceResponse(status_code=status.HTTP_200_OK, content=f"The column '{target_column}' is set as target for"
                                                                   f" '{filename}'")


@documents_method_router.get("/column_marks", response_model=ColumnMarks)
def read_column_marks(filename: str, db: get_db = Depends(), user: User = Depends(current_active_user)):
    result = DocumentService(db, user).read_column_marks(filename)
    return result


@documents_method_router.post("/apply/delete_column", response_model=ServiceResponse)
def delete_column(filename: str, column_name: str, db: get_db = Depends(), user: User = Depends(current_active_user)):
    result = DocumentService(db, user).apply_function(filename, function_name='drop_column', param=column_name)
    if result:
        return ServiceResponse(status_code=status.HTTP_200_OK, content=f"The column '{column_name}' successfully "
                                                                       f"deleted")
    else:
        return ServiceResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=f"Error with deletion")


@documents_method_router.post("/apply/method", response_model=ServiceResponse)
def apply_method(filename: str, function_name: AvailableFunctions, db: get_db = Depends(),
                 user: User = Depends(current_active_user)):
    result = DocumentService(db, user).apply_function(filename, function_name=function_name.value)
    if result:
        return ServiceResponse(status_code=status.HTTP_200_OK, content=f"The method '{function_name}' successfully "
                                                                       f"applied")
    else:
        return ServiceResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=f"Error with applying")


@documents_method_router.put("/apply/pipeline", response_model=ServiceResponse)
def copy_pipeline(from_document: str, to_document: str, db: get_db = Depends(),
                  user: User = Depends(current_active_user)):
    DocumentService(db, user).copy_and_apply_pipeline_to_another_document(filename_orig=from_document,
                                                                          filename_new=to_document)
    return ServiceResponse(status_code=status.HTTP_200_OK, content=f"Pipeline from '{from_document}' applied to "
                                                                   f"'{to_document}'")

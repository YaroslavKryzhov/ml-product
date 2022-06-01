from typing import List, Optional

from fastapi import APIRouter, Depends, UploadFile, File, status

from ml_api.common.database.db_deps import get_db
from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.models import User
from ml_api.apps.documents.services import DocumentService
from ml_api.apps.documents.schemas import DocumentFullInfo, DocumentShortInfo, AvailableFunctions, \
    ServiceResponse, ReadDocumentResponse, TaskType, ColumnDescription, DocumentDescription
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
        return ServiceResponse(status_code=status.HTTP_409_CONFLICT, content="Error with deletion")
# f"The document '{filename}' is is used in some model!"


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


@documents_df_router.get("/info", response_model=List[ColumnDescription])
def document_columns_stat_info(filename: str, db: get_db = Depends(), user: User = Depends(current_active_user)):
    result = DocumentService(db, user).get_document_columns_info(filename)
    return result


@documents_df_router.get("/describe", response_model=DocumentDescription)
def document_stat_describe(filename: str, db: get_db = Depends(), user: User = Depends(current_active_user)):
    result = DocumentService(db, user).get_document_stat_description(filename)
    return result


@documents_df_router.get("/columns", response_model=List[str])
def get_column_names(filename: str, db: get_db = Depends(), user: User = Depends(current_active_user)):
    result = DocumentService(db, user).read_document_columns(filename)
    return result


documents_method_router = APIRouter(
    prefix="/document/edit",
    tags=["Document Editions"],
    responses={404: {"description": "Not found"}}
)


@documents_method_router.post("/target", response_model=ServiceResponse)
def set_target_feature(filename: str, target_column: str, task_type: TaskType, db: get_db = Depends(),
                       user: User = Depends(current_active_user)):
    DocumentService(db, user).set_column_types(filename, target_column, task_type)
    return ServiceResponse(status_code=status.HTTP_200_OK, content=f"The column '{target_column}' is set as target for"
                                                                   f" '{filename}'")


@documents_method_router.post("/to_categorical", response_model=ServiceResponse)
def set_column_as_categorical(filename: str, column_name: str, db: get_db = Depends(),
                              user: User = Depends(current_active_user)):
    result = DocumentService(db, user).set_column_as_categorical(filename, column_name)
    if result:
        return ServiceResponse(status_code=status.HTTP_200_OK,
                               content=f"The column '{column_name}' is set as categorical for '{filename}'")
    else:
        return ServiceResponse(status_code=status.HTTP_409_CONFLICT,
                               content=f"The column '{column_name}' can't be set as categorical for '{filename}'")


@documents_method_router.post("/to_numeric", response_model=ServiceResponse)
def set_column_as_numeric(filename: str, column_name: str, db: get_db = Depends(),
                          user: User = Depends(current_active_user)):
    result = DocumentService(db, user).set_column_as_numeric(filename, column_name)
    if result:
        return ServiceResponse(status_code=status.HTTP_200_OK,
                               content=f"The column '{column_name}' is set as numeric for '{filename}'")
    else:
        return ServiceResponse(status_code=status.HTTP_409_CONFLICT,
                               content=f"The column '{column_name}' can't be set as numeric for '{filename}'")


@documents_method_router.delete("/column", response_model=ServiceResponse)
def delete_column(filename: str, column_name: str, db: get_db = Depends(), user: User = Depends(current_active_user)):
    result = DocumentService(db, user).apply_function(filename, function_name='drop_column', param=column_name)
    if result:
        return ServiceResponse(status_code=status.HTTP_200_OK, content=f"The column '{column_name}' successfully "
                                                                       f"deleted")
    else:
        return ServiceResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=f"Error with deletion")


@documents_method_router.put("/apply_method", response_model=ServiceResponse)
def apply_method(filename: str, function_name: AvailableFunctions, param: Optional[float] = None,
                 db: get_db = Depends(), user: User = Depends(current_active_user)):
    result = DocumentService(db, user).apply_function(filename, function_name=function_name.value, param=param)
    if result:
        return ServiceResponse(status_code=status.HTTP_200_OK, content=f"The method '{function_name.value}' "
                                                                       f"successfully applied")
    else:
        return ServiceResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=f"Error with applying")


@documents_method_router.put("/copy_pipeline", response_model=ServiceResponse)
def copy_pipeline(from_document: str, to_document: str, db: get_db = Depends(),
                  user: User = Depends(current_active_user)):
    DocumentService(db, user).copy_and_apply_pipeline_to_another_document(filename_orig=from_document,
                                                                          filename_new=to_document)
    return ServiceResponse(status_code=status.HTTP_200_OK, content=f"Pipeline from '{from_document}' applied to "
                                                                   f"'{to_document}'")

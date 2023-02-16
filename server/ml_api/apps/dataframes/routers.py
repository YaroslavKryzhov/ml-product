from typing import List, Any
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, status, Response

from ml_api.common.dependencies.db_deps import get_db
from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.models import User
from ml_api.apps.dataframes.services import DataframeManagerService
from ml_api.apps.dataframes import schemas
from ml_api.apps.dataframes.specs import specs
from ml_api.common.celery_tasks.celery_worker import apply_function_celery
from ml_api.common.celery_tasks.schemas import TaskJwtResponse
from ml_api.common.security.token_utils import create_centrifugo_token

dataframes_file_router = APIRouter(
    prefix="/dataframe",
    tags=["Dataframe As File"],
    responses={404: {"description": "Not found"}},
)


@dataframes_file_router.post("")
def upload_document(
    filename: str,
    file: UploadFile = File(...),
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    dataframe_id = DataframeManagerService(db, user.id).upload_file(
        file=file.file, filename=filename
    )
    return Response(
        status_code=status.HTTP_200_OK,
        content=dataframe_id,
        media_type='text/plain',
    )


@dataframes_file_router.get("/download")
def download_document(
    dataframe_id: UUID,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    result = DataframeManagerService(db, user.id).download_file(dataframe_id)
    return result


@dataframes_file_router.put("/rename")
def rename_document(
    dataframe_id: UUID,
    new_filename: str,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    DataframeManagerService(db, user.id).rename_file(
        dataframe_id, new_filename
    )
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"Document with id {dataframe_id} successfully renamed to '{new_filename}'.",
        media_type='text/plain',
    )


@dataframes_file_router.delete("")
def delete_document(
    dataframe_id: UUID,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    DataframeManagerService(db, user.id).delete_file(dataframe_id)
    return Response(
        status_code=status.HTTP_200_OK,
        content=str(dataframe_id),
        media_type='text/plain',
    )


@dataframes_file_router.get("", response_model=schemas.DataFrameInfo)
def read_document_info(
    dataframe_id: UUID,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    return DataframeManagerService(db, user.id
        ).get_dataframe_info(dataframe_id)


@dataframes_file_router.get("/all", response_model=List[schemas.DataFrameInfo])
def read_all_user_documents(
    db: get_db = Depends(), user: User = Depends(current_active_user)
):
    return DataframeManagerService(db, user.id).get_all_dataframes_info()


documents_df_router = APIRouter(
    prefix="/dataframe/df",
    tags=["Dataframe As pandas.DataFrame"],
    responses={404: {"description": "Not found"}},
)


@documents_df_router.get("", response_model=schemas.ReadDataFrameResponse)
def read_document_with_pagination(
    dataframe_id: UUID,
    page: int = 1,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    return DataframeManagerService(db, user.id
        ).get_dataframe_with_pagination(dataframe_id, page)


@documents_df_router.get("/statistics",
                         response_model=List[schemas.ColumnDescription])
def document_columns_stat_info(
    dataframe_id: UUID,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    return DataframeManagerService(db, user.id
        ).get_dataframe_column_statistics(dataframe_id)


@documents_df_router.get("/describe",
                         response_model=schemas.DataFrameDescription)
def document_stat_describe(
    dataframe_id: UUID,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    return DataframeManagerService(db, user.id
        ).get_dataframe_statistic_description(dataframe_id)


@documents_df_router.get("/columns", response_model=List[str])
def get_column_names(
    dataframe_id: UUID,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    return DataframeManagerService(db, user.id
        ).get_dataframe_columns(dataframe_id)


documents_method_router = APIRouter(
    prefix="/dataframe/edit",
    tags=["Dataframe Editions"],
    responses={404: {"description": "Not found"}},
)


@documents_method_router.put("/target")
def set_target_feature(
    dataframe_id: UUID,
    target_column: str,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    DataframeManagerService(db, user.id).set_target_column(
        dataframe_id, target_column)

    return Response(
        status_code=status.HTTP_200_OK,
        content=f"The column '{target_column}' is set as target.",
        media_type='text/plain',
    )


@documents_method_router.put("/to_categorical")
def set_column_as_categorical(
    dataframe_id: UUID,
    column_name: str,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    DataframeManagerService(db, user.id
        ).change_column_type_to_categorical(dataframe_id, column_name)
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"The column '{column_name}' is set as categorical",
        media_type='text/plain',
    )


@documents_method_router.put("/to_numeric")
def set_column_as_numeric(
    dataframe_id: UUID,
    column_name: str,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    DataframeManagerService(db, user.id
        ).change_column_type_to_numeric(dataframe_id, column_name)
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"The column '{column_name}' is set as numeric",
        media_type='text/plain',
    )


@documents_method_router.delete("/column")
def delete_column(
    dataframe_id: UUID,
    column_name: str,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    DataframeManagerService(db, user.id).apply_function(
        dataframe_id, specs.AvailableFunctions.drop_column, column_name
    )
    return Response(
        status_code=status.HTTP_200_OK,
        content=f"The column '{column_name}' successfully deleted",
        media_type='text/plain',
    )


@documents_method_router.post("/apply_method")
def apply_method(
    dataframe_id: UUID,
    function_name: specs.AvailableFunctions,
    params: Any = None,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    DataframeManagerService(db, user.id).get_dataframe_info(dataframe_id)

    task = apply_function_celery.delay(str(user.id),
        str(dataframe_id), function_name.value, params)

    jwt_token = create_centrifugo_token(user.id)

    return TaskJwtResponse(
        task_id=task.id,
        jwt_token=jwt_token,
    )


@documents_method_router.post("/copy_pipeline")
def copy_pipeline(
    dataframe_id_from: UUID,
    dataframe_id_to: UUID,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    # task = copy_pipeline_celery.delay(from_document, to_document)
    # jwt_token = create_centrifugo_token(user.id)
    DataframeManagerService(db, user.id).copy_pipeline(dataframe_id_from,
                                                       dataframe_id_to)
    return Response(
        status_code=status.HTTP_200_OK,
        content="task_id",
        media_type='text/plain',
    )

from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.models import User
from ml_api.apps.ml_models.services.file_manager import ModelFileManagerService
from ml_api.apps.ml_models.services.metadata_manager import ModelMetadataManagerService
from ml_api.apps.ml_models.services.processing_manager import ModelProcessingManagerService
from ml_api.apps.ml_models import schemas, specs, models
# from ml_api.common.celery_tasks.celery_tasks import train_composition_celery

models_file_router = APIRouter(
    prefix="/models",
    tags=["Models"],
    responses={404: {"description": "Not found"}},
)


@models_file_router.get("/download", summary="Скачать модель")
def download_model(
    model_id: PydanticObjectId,
    model_format: specs.ModelFormats = specs.ModelFormats.PICKLE,
    user: User = Depends(current_active_user),
):
    """
        Скачивает модель в формате, указанном в параметре model_format.

        - **model_id**: ID модели
        - **model_format**: Формат модели, в котором она будет скачана.
    """
    result = ModelFileManagerService(user.id).download_file(model_id, model_format)
    return result


@models_file_router.put("/rename", summary="Переименовать модель",
                   response_model=models.ModelMetadata)
def rename_model(
    model_id: PydanticObjectId,
    new_model_name: str,
    user: User = Depends(current_active_user),
):
    """
        Переименовывает модель.

        - **model_id**: ID модели
        - **new_model_name**: новое имя модели
    """
    return await ModelMetadataManagerService(user.id).set_filename(
        model_id, new_model_name)


@models_file_router.delete("",  summary="Удалить модель",
                           response_model=models.ModelMetadata)
def delete_model(
    model_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Удаляет модель.

        - **model_id**: ID модели
    """
    return await ModelFileManagerService(user.id).delete_file(model_id)


models_metadata_router = APIRouter(
    prefix="/models/metadata",
    tags=["Models Metadata"],
    responses={404: {"description": "Not found"}},
)


@models_metadata_router.get("", response_model=models.ModelMetadata,
    summary="Получить информацию о модели")
def read_model_info(
    model_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Возвращает информацию о модели.

        - **model_id**: ID модели
    """
    return await ModelMetadataManagerService(user.id).get_model_meta(model_id)


@models_metadata_router.get("/all", response_model=List[models.ModelMetadata],
    summary="Получить информацию обо всех моделях пользователя")
def read_all_user_models(user: User = Depends(current_active_user)):
    """
        Возвращает информацию обо всех моделях пользователя
    """
    return await ModelMetadataManagerService(user.id).get_all_models_meta()


@models_metadata_router.get("/by_dataframe",
                            response_model=List[models.ModelMetadata],
    summary="Получить информацию обо всех моделях обученных на датафрейме")
def read_all_user_compositions(
        dataframe_id: PydanticObjectId,
        user: User = Depends(current_active_user)
):
    return await ModelMetadataManagerService(
        user.id).get_all_models_meta_by_dataframe(dataframe_id=dataframe_id)


models_processing_router = APIRouter(
    prefix="/models/processing",
    tags=["Models Metadata"],
    responses={404: {"description": "Not found"}},
)


@models_processing_router.post("/train")
def train_model(model_name: str,
                dataframe_id: PydanticObjectId,
                task_type: specs.AvailableTaskTypes,
                model_params: schemas.ModelParams,
                params_type: specs.AvailableParamsTypes,
                test_size: float = 0.2,
                user: User = Depends(current_active_user)):
    model_meta = await ModelMetadataManagerService(user.id).create_model(
        model_name=model_name,
        dataframe_id=dataframe_id,
        task_type=task_type,
        model_params=model_params,
        params_type=params_type,
        test_size=test_size)
    model = await ModelProcessingManagerService(user.id).prepare_model(
        model_meta=model_meta)
    result = await ModelProcessingManagerService(user.id).train_model(
        model_meta=model_meta, model=model)
    return result
    # task = train_composition_celery.delay(
    #     str(user.id), str(model_info.id), params_type.value, test_size)
    # return task.id


@models_processing_router.get("/predict")
def predict_on_model(dataframe_id: PydanticObjectId,
            model_id: PydanticObjectId,
            user: User = Depends(current_active_user)):
    result = ModelProcessingManagerService(user.id).predict_on_model(
        dataframe_id=dataframe_id, model_id=model_id)
    return result

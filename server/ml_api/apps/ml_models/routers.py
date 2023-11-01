from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.model import User
from ml_api.apps.ml_models import schemas, specs, model
from ml_api.apps.ml_models.services.model_service import ModelService
from ml_api.apps.ml_models.services.fit_predict_service import ModelFitPredictService
# from ml_api.common.celery_tasks.celery_tasks import train_composition_celery

models_file_router = APIRouter(
    prefix="/model",
    tags=["Models"],
    responses={404: {"description": "Not found"}},
)


@models_file_router.get("/download", summary="Скачать модель")
async def download_model(
    model_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Скачивает модель.

        - **model_id**: ID модели
    """
    return await ModelService(user.id).download_model(model_id)


@models_file_router.put("/rename", summary="Переименовать модель",
                   response_model=model.ModelMetadata)
async def rename_model(
    model_id: PydanticObjectId,
    new_model_name: str,
    user: User = Depends(current_active_user),
):
    """
        Переименовывает модель.

        - **model_id**: ID модели
        - **new_model_name**: новое имя модели
    """
    return await ModelService(user.id).set_filename(
        model_id, new_model_name)


@models_file_router.delete("",  summary="Удалить модель",
                           response_model=model.ModelMetadata)
async def delete_model(
    model_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Удаляет модель.

        - **model_id**: ID модели
    """
    return await ModelService(user.id).delete_model(model_id)


models_metadata_router = APIRouter(
    prefix="/model/metadata",
    tags=["Models Metadata"],
    responses={404: {"description": "Not found"}},
)


@models_metadata_router.get("", response_model=model.ModelMetadata,
    summary="Получить информацию о модели")
async def read_model_info(
    model_id: PydanticObjectId,
    user: User = Depends(current_active_user),
):
    """
        Возвращает информацию о модели.

        - **model_id**: ID модели
    """
    return await ModelService(user.id).get_model_meta(model_id)


@models_metadata_router.get("/all", response_model=List[model.ModelMetadata],
    summary="Получить информацию обо всех моделях пользователя")
async def read_all_user_models(user: User = Depends(current_active_user)):
    """
        Возвращает информацию обо всех моделях пользователя
    """
    return await ModelService(user.id).get_all_models_meta()


@models_metadata_router.get("/by_dataframe",
                            response_model=List[model.ModelMetadata],
    summary="Получить информацию обо всех моделях обученных на датафрейме")
async def read_all_user_models_by_dataframe(
        dataframe_id: PydanticObjectId,
        user: User = Depends(current_active_user)
):
    """
        Возвращает информацию обо всех моделях пользователя,
        обученных на данном датафрейме

        - **dataframe_id**: ID датафрейма
    """
    return await ModelService(
        user.id).get_all_models_meta_by_dataframe(dataframe_id=dataframe_id)


models_processing_router = APIRouter(
    prefix="/model/processing",
    tags=["Models Processing"],
    responses={404: {"description": "Not found"}},
)


@models_processing_router.post("/train")
async def train_model(model_name: str,
                dataframe_id: PydanticObjectId,
                task_type: specs.AvailableTaskTypes,
                model_params: schemas.ModelParams,
                params_type: specs.AvailableParamsTypes,
                test_size: float = None,
                stratify: bool = None,
                user: User = Depends(current_active_user)):
    """
        Запускает обучение модели.

        - **model_name**: имя новой модели
        - **dataframe_id**: ID датафрейма
        - **task_type**: тип задачи
        - **model_params**: тип и гиперпараметры модели
        - **params_type**: тип подбора параметров (авто(hyperopt) только для
        классификации/регрессии/кластеризации)
        - **test_size**: размер валидационной выборки (классификация/регрессия)
        - **stratify**: делать ли стратификацию (при классификации)
    """
    model_meta = await ModelService(user.id).create_model(
        model_name=model_name,
        dataframe_id=dataframe_id,
        task_type=task_type,
        model_params=model_params,
        params_type=params_type,
        test_size=test_size,
        stratify=stratify)
    return await ModelFitPredictService(
        user.id).train_model(model_meta=model_meta)
    # task = train_composition_celery.delay(
    #     str(user.id), str(model_info.id), params_type.value, test_size)
    # return task.id


@models_processing_router.post("/build_composition")
async def train_model(composition_name: str,
                      model_ids: List[PydanticObjectId],
                      composition_params: schemas.ModelParams,
                user: User = Depends(current_active_user)):
    composition_meta = await ModelService(user.id).create_composition(
        composition_name=composition_name, model_ids=model_ids,
        composition_params=composition_params)
    return await ModelFitPredictService(
        user.id).train_composition(composition_meta=composition_meta)
    # task = train_composition_celery.delay(
    #     str(user.id), str(model_info.id), params_type.value, test_size)
    # return task.id


@models_processing_router.put("/predict")
async def predict_on_model(dataframe_id: PydanticObjectId,
            model_id: PydanticObjectId,
            apply_pipeline: bool = True,
            user: User = Depends(current_active_user)):
    """
        Делает предсказание на модели.

        - **dataframe_id**: ID датафрейма
        - **model_id**: ID модели
        - **apply_pipeline**: применять ли пайплайн с выборки, на которой
        училась модель

        Если данные в сыром виде, можно скопировать пайплайн с
        оригинальной выборки перед предсказанием.
        Если данные уже предобработаны, можно поставить параметр = False.
    """
    return await ModelFitPredictService(user.id).predict_on_model(
        source_df_id=dataframe_id,
        model_id=model_id,
        apply_pipeline=apply_pipeline)

from fastapi import APIRouter, Depends, BackgroundTasks
from typing import List

from ml_api.common.database.db_deps import get_db
from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.models import User
from ml_api.apps.ml_models.services import ModelService
from ml_api.apps.ml_models.schemas import (
    AvailableParams,
    AvailableTaskTypes,
    AvailableCompositions,
    CompositionParams,
    CompositionShortInfoResponse,
    CompositionFullInfoResponse,
)

models_router = APIRouter(
    prefix="/composition",
    tags=["Compositions"],
    responses={404: {"description": "Not found"}},
)


@models_router.post("/train")
def train_composition(  # task_type: AvailableTaskTypes,
    composition_type: AvailableCompositions,
    composition_params: List[CompositionParams],
    params_type: AvailableParams,
    document_name: str,
    model_name: str,
    background_tasks: BackgroundTasks,
    test_size: float = 0.2,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    result = ModelService(db, user).train_model(
        task_type=AvailableTaskTypes.CLASSIFICATION.value,
        composition_type=composition_type.value,
        composition_params=composition_params,
        params_type=params_type.value,
        document_name=document_name,
        model_name=model_name,
        background_tasks=background_tasks,
        test_size=test_size,
    )
    return result


@models_router.get("/predict")
def predict(
    document_name: str,
    model_name: str,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    result = ModelService(db, user).predict_on_model(
        filename=document_name, model_name=model_name
    )
    return result


@models_router.get("/download")
def download_composition(
    model_name: str,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    result = ModelService(db, user).download_model(model_name)
    return result


@models_router.put("/rename")
def rename_composition(
    model_name: str,
    new_model_name: str,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    ModelService(db, user).rename_model(model_name, new_model_name)
    return {"filename": new_model_name}


@models_router.delete("")
def delete_composition(
    model_name: str,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    ModelService(db, user).delete_model(model_name)
    return {"filename": model_name}


@models_router.get("/all")
def read_all_user_compositions(
    db: get_db = Depends(), user: User = Depends(current_active_user)
):
    result = ModelService(db, user).read_models_info()
    return result


@models_router.get("/info")
def read_composition_info(
    model_name: str,
    db: get_db = Depends(),
    user: User = Depends(current_active_user),
):
    result = ModelService(db, user).read_model_info(model_name=model_name)
    return result

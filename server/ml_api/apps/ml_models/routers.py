from fastapi import APIRouter, Depends
from typing import Dict, Any

from ml_api.common.database.db_deps import get_db
from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.schemas import UserDB
from ml_api.apps.ml_models.services import ModelService
from ml_api.apps.ml_models.configs.classification_models_config import AvailableModels
from ml_api.apps.ml_models.schemas import AvailableSplits

models_router = APIRouter(
    prefix="/models",
    tags=["Model Training"],
    responses={404: {"description": "Not found"}}
)


@models_router.post("/train")
def train_model(filename: str, model_type: AvailableModels, model_name: str, params: Dict[str, Any],
                split_type: AvailableSplits, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    result = ModelService(db, user).train_classification_model(filename, params=params, model_type=model_type,
                                                               model_name=model_name,
                                                               split_type=split_type)
    return result


@models_router.get("/predict_tree")
def predict(filename: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    predictions = ModelService(db, user).predict_on_model(filename)
    return {"predictions": predictions}


@models_router.get("/download")
def download_document(model_name: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    result = ModelService(db, user).download_model_from_db(model_name)
    return result


@models_router.put("/rename")
def rename_document(model_name: str, new_model_name: str, db: get_db = Depends(),
                    user: UserDB = Depends(current_active_user)):
    ModelService(db, user).rename_model(model_name, new_model_name)
    return {"filename": new_model_name}


@models_router.delete("")
def delete_document(model_name: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    ModelService(db, user).delete_model_from_db(model_name)
    return {"filename": model_name}

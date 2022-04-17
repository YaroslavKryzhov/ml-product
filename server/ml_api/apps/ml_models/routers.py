from fastapi import APIRouter, Depends

from ml_api.common.database.db_deps import get_db
from ml_api.apps.users.routers import current_active_user
from ml_api.apps.users.schemas import UserDB
from ml_api.apps.ml_models.services import ModelService
from ml_api.apps.ml_models.configs.classification_models_config import DecisionTreeClassifierParameters, AvailableModels



models_router = APIRouter(
    prefix="/models",
    tags=["Model Training"],
    responses={404: {"description": "Not found"}}
)


@models_router.post("/train_tree")
def train_tree(filename: str, model: AvailableModels, params: DecisionTreeClassifierParameters, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    score = ModelService(db, user).train_model(filename, params=params, model=model)
    return {"score": score}


@models_router.get("/predict_tree")
def predict(filename: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    predictions = ModelService(db, user).predict_on_model(filename)
    return {"predictions": predictions}


@models_router.get("/download")
def download_document(model_name: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    result = ModelService(db, user).download_model_from_db(model_name)
    return result


@models_router.put("/rename")
def rename_document(model_name: str, new_model_name: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    ModelService(db, user).rename_model(model_name, new_model_name)
    return {"filename": new_model_name}


@models_router.delete("")
def delete_document(model_name: str, db: get_db = Depends(), user: UserDB = Depends(current_active_user)):
    ModelService(db, user).delete_model_from_db(model_name)
    return {"filename": model_name}

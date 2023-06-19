# from typing import List
# from uuid import UUID
#
# from fastapi import APIRouter, Depends, status, Response
#
# from ml_api.common.dependencies.db_deps import get_db
# from ml_api.apps.users.routers import current_active_user
# from ml_api.apps.users.models import User
# from ml_api.apps.ml_models.services.services import ModelManagerService
# from ml_api.apps.ml_models import schemas, specs
# from ml_api.common.celery_tasks.celery_tasks import train_composition_celery
#
# models_router = APIRouter(
#     prefix="/composition",
#     tags=["Compositions"],
#     responses={404: {"description": "Not found"}},
# )
#
#
# @models_router.get("/download")
# def download_composition(
#     model_id: UUID,
#     db: get_db = Depends(),
#     user: User = Depends(current_active_user),
# ):
#     result = ModelManagerService(db, user.id).download_model(model_id)
#     return result
#
#
# @models_router.put("/rename")
# def rename_composition(
#     model_id: UUID,
#     new_model_name: str,
#     db: get_db = Depends(),
#     user: User = Depends(current_active_user),
# ):
#     ModelManagerService(db, user.id).rename_model(model_id, new_model_name)
#     return Response(
#         status_code=status.HTTP_200_OK,
#         content=f"Composition with id {model_id} successfully renamed to '{new_model_name}'.",
#         media_type='text/plain',
#     )
#
#
# @models_router.delete("")
# def delete_composition(
#     model_id: UUID,
#     db: get_db = Depends(),
#     user: User = Depends(current_active_user),
# ):
#     ModelManagerService(db, user.id).delete_model(model_id)
#     return Response(
#         status_code=status.HTTP_200_OK,
#         content=str(model_id),
#         media_type='text/plain',
#     )
#
#
# @models_router.get("", response_model=schemas.CompositionInfo)
# def read_composition_info(
#     model_id: UUID,
#     db: get_db = Depends(),
#     user: User = Depends(current_active_user),
# ):
#     return ModelManagerService(db, user.id).get_model_info(model_id=model_id)
#
#
# @models_router.get("/all", response_model=List[schemas.CompositionInfo])
# def read_all_user_compositions(
#     db: get_db = Depends(), user: User = Depends(current_active_user)
# ):
#     return ModelManagerService(db, user.id).get_all_models_info()
#
#
# @models_router.post("/train")
# def train_composition(
#     task_type: specs.AvailableTaskTypes,
#     composition_type: specs.AvailableCompositionTypes,
#     composition_params: List[schemas.CompositionParams],
#     params_type: specs.AvailableParamsTypes,
#     dataframe_id: UUID,
#     model_name: str,
#     test_size: float = 0.2,
#     save_format: specs.ModelSaveFormats = specs.ModelSaveFormats.ONNX,
#     db: get_db = Depends(),
#     user: User = Depends(current_active_user),
# ):
#     model_info = ModelManagerService(db, user.id).create_model(
#         task_type=task_type,
#         composition_type=composition_type,
#         composition_params=composition_params,
#         dataframe_id=dataframe_id,
#         model_name=model_name,
#         save_format=save_format
#     )
#     # model = ModelManagerService(db, user.id).prepare_model(
#     #     model_info=model_info,
#     #     params_type=params_type,
#     # )
#     # ModelManagerService(db, user.id).train_model(
#     #     model_info=model_info,
#     #     composition=model,
#     #     test_size=test_size
#     # )
#     task = train_composition_celery.delay(
#         str(user.id), str(model_info.id), params_type.value, test_size)
#     return task.id
#
#
# @models_router.get("/predict")
# def predict(
#     dataframe_id: UUID,
#     model_id: UUID,
#     db: get_db = Depends(),
#     user: User = Depends(current_active_user),
# ):
#     result = ModelManagerService(db, user.id).predict_on_model(
#         dataframe_id=dataframe_id, model_id=model_id)
#     return result

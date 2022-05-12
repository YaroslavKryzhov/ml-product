from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ml_api.common import config
from ml_api.apps.documents.routers import documents_crud_router, documents_method_router
from ml_api.apps.users.routers import users_router
from ml_api.apps.ml_models.routers import models_router


app = FastAPI(title=config.PROJECT_NAME,
              version=config.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.exception_handler(AppExceptionCase)
# async def custom_app_exception_handler(request, e):
#     return await app_exception_handler(request, e)

app.include_router(documents_crud_router)
app.include_router(documents_method_router)
app.include_router(users_router)
app.include_router(models_router)

import fastapi
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from ml_api import config
from ml_api.apps.dataframes.controller.routers import (
    documents_file_router,
    documents_df_router,
    documents_method_router,
)
from ml_api.apps.users.controller.routers import users_router
from ml_api.apps.ml_models.controller.routers import models_router

if config.STAGE.upper() == 'PRODUCTION':
    docs_url = None
    openapi_url = None
else:
    docs_url = config.DOCS_URL
    openapi_url = config.OPENAPI_URL

app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.VERSION,
    docs_url=docs_url,
    openapi_url=openapi_url,
)

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

api_router = APIRouter(prefix=config.API_PREFIX)
api_router.include_router(documents_file_router)
api_router.include_router(documents_df_router)
api_router.include_router(documents_method_router)
api_router.include_router(users_router)
api_router.include_router(models_router)
app.include_router(api_router)

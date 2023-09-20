from fastapi import FastAPI, APIRouter, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from ml_api import config
from ml_api.apps.users.routers import users_router
from ml_api.apps.dataframes.routers import (
    dataframes_file_router,
    dataframes_metadata_router,
    dataframes_content_router,
    dataframes_methods_router)
from ml_api.apps.ml_models.routers import (
    models_file_router,
    models_metadata_router,
    models_processing_router)
from ml_api.apps.training_reports.routers import reports_router

from ml_api.apps.users.models import User
from ml_api.apps.dataframes.models import DataFrameMetadata
from ml_api.apps.ml_models.models import ModelMetadata
from ml_api.apps.training_reports.models import Report

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


# @app.exception_handler(ApplyFunctionException)
# async def unicorn_exception_handler(request: Request, exc: ApplyFunctionException):
#     return JSONResponse(
#         status_code=status.HTTP_404_NOT_FOUND,
#         content=str(exc),
#     )


@app.on_event("startup")
async def app_init():
    """Initialize application services"""
    app.db = AsyncIOMotorClient(config.MONGO_DATABASE_URI,
                                uuidRepresentation="standard")[config.MONGO_DEFAULT_DB_NAME]
    try:
        await init_beanie(app.db,
            document_models=[User, DataFrameMetadata, ModelMetadata, Report])
    except ServerSelectionTimeoutError as sste:
        print(sste)


api_router = APIRouter(prefix=config.API_PREFIX)
api_router.include_router(users_router)
api_router.include_router(dataframes_file_router)
api_router.include_router(dataframes_metadata_router)
api_router.include_router(dataframes_content_router)
api_router.include_router(dataframes_methods_router)
api_router.include_router(models_file_router)
api_router.include_router(models_metadata_router)
api_router.include_router(models_processing_router)
api_router.include_router(reports_router)
app.include_router(api_router)

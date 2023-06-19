from fastapi import FastAPI, APIRouter, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from ml_api import config
from ml_api.apps.dataframes.routers import (
    dataframes_file_router,
    # dataframes_df_router,
    # dataframes_method_router,
)
from ml_api.apps.dataframes.services.methods_processor import ApplyFunctionException
from ml_api.apps.users.routers import users_router
# from ml_api.apps.ml_models.routers import models_router

from ml_api.apps.dataframes.models import DataFrameMetadata
from ml_api.apps.users.models import User

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


@app.exception_handler(ApplyFunctionException)
async def unicorn_exception_handler(request: Request, exc: ApplyFunctionException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=str(exc),
    )


@app.on_event("startup")
async def app_init():
    """Initialize application services"""
    app.db = AsyncIOMotorClient(config.MONGO_DATABASE_URI,
                                uuidRepresentation="standard")[config.MONGO_DEFAULT_DB_NAME]
    await init_beanie(app.db, document_models=[User, DataFrameMetadata])


api_router = APIRouter(prefix=config.API_PREFIX)
api_router.include_router(dataframes_file_router)
# api_router.include_router(dataframes_df_router)
# api_router.include_router(dataframes_method_router)
api_router.include_router(users_router)
# api_router.include_router(models_router)
app.include_router(api_router)

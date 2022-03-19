from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ml_api.common import config
from ml_api.apps.csv.routers import csv_router

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

app.include_router(csv_router)
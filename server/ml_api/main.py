from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ml_api.common import config
from ml_api.apps.documents.routers import documents_router
from ml_api.apps.users.routers import fastapi_users, auth_backend, users_router


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

app.include_router(documents_router)
app.include_router(users_router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"],
)

import uuid
from fastapi_users import FastAPIUsers
from fastapi import APIRouter
from ml_api.apps.users.schemas import UserCreate, UserRead
from ml_api.apps.users.models import User
from ml_api.apps.users.services import get_user_manager, auth_backend

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)

users_router = APIRouter(
    tags=["Users"], responses={404: {"description": "Not found"}}
)

users_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt"
)

users_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth"
)

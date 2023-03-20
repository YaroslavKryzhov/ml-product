import uuid

from fastapi_users import FastAPIUsers
from fastapi import APIRouter, Depends

from ml_api.apps.users.schemas import UserCreate, UserRead
from ml_api.apps.users.models import User
from ml_api.apps.users.services import get_user_manager, auth_backend
from ml_api.common.security.token_utils import create_centrifugo_token

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)

users_router = APIRouter(
    tags=["Users"], responses={404: {"description": "Not found"}}
)


@users_router.get("/auth/centrifugo_token")
def get_centrifugo_token(user: User = Depends(current_active_user)):
    jwt_token = create_centrifugo_token(str(user.id))
    return jwt_token


users_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt"
)

users_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth"
)

# users_router.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"],
# )

# users_router.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
# )

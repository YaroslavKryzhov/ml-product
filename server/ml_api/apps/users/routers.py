from fastapi import APIRouter, Depends

from ml_api.apps.users.schemas import UserCreate, UserRead
from ml_api.apps.users.models import User
from ml_api.apps.users.services import fastapi_users, auth_backend, current_active_user
from ml_api.common.security.token_utils import create_centrifugo_token


users_router = APIRouter(
    tags=["Users"], responses={404: {"description": "Not found"}}
)


@users_router.get("/auth/centrifugo_token")
def get_centrifugo_token(user: User = Depends(current_active_user)):
    jwt_token = create_centrifugo_token(str(user.id))
    return jwt_token


@users_router.get("/auth/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}! Your id is {user.id}"}


users_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt"
)

users_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth"
)

# users_router.include_router(
#     fastapi_users.get_reset_password_router(), prefix="/auth",
# )
# users_router.include_router(
#     fastapi_users.get_verify_router(UserRead), prefix="/auth",
# )
# users_router.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users",
# )

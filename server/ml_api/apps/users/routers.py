from fastapi import APIRouter, Depends

from ml_api.apps.users.schemas import UserCreate, UserRead, JWTToken, GetId
from ml_api.apps.users.model import User
from ml_api.apps.users.services import fastapi_users, auth_backend, current_active_user
from ml_api.common.pubsub.token_utils import create_centrifugo_token


users_router = APIRouter(
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    prefix="/auth"
)


@users_router.get("/centrifugo_token", response_model=JWTToken)
def get_centrifugo_token(user: User = Depends(current_active_user)):
    """
        Возращает токен для подключения к каналам Centrifugo
    """
    jwt_token = create_centrifugo_token(str(user.id))
    return JWTToken(token=jwt_token, user_id=str(user.id))


users_router.include_router(
    fastapi_users.get_auth_router(auth_backend)
)

users_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate)
)

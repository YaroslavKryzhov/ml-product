from fastapi_users import FastAPIUsers
from fastapi import APIRouter, Depends
from ml_api.apps.users.schemas import User, UserDB, UserUpdate, UserCreate
from ml_api.apps.users.services import get_user_manager, auth_backend

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

current_active_user = fastapi_users.current_user(active=True)


users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)


@users_router.get("/authenticated-route")
async def authenticated_route(user: UserDB = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
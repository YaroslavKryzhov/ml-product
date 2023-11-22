from typing import Optional
from pydantic import BaseModel, EmailStr
from beanie import PydanticObjectId


class CreateUpdateDictModel(BaseModel):
    def create_update_dict(self):
        return self.dict(exclude_unset=True, exclude={"id"})

    def create_update_dict_superuser(self):
        return self.dict(exclude_unset=True, exclude={"id"})


class UserRead(CreateUpdateDictModel):
    id: PydanticObjectId
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(CreateUpdateDictModel):
    email: EmailStr
    password: str


class UserUpdate(CreateUpdateDictModel):
    password: Optional[str]
    email: Optional[EmailStr]


class JWTToken(BaseModel):
    token: str


class GetId(BaseModel):
    user_id: str

# from fastapi_users import schemas
#
#
# class UserRead(schemas.BaseUser[PydancticObjectId]):
#     pass
#
#
# class UserCreate(schemas.BaseUserCreate):
#     pass
#
#
# class UserUpdate(schemas.BaseUserUpdate):
#     pass

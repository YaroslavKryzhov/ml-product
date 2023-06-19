from beanie import Document
from fastapi_users.db import BeanieBaseUser


class User(BeanieBaseUser, Document):
    pass

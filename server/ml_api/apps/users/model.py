from bunnet import Document
from pydantic import BaseModel
from pymongo import IndexModel
from pymongo.collation import Collation


class BunnetBaseUser(BaseModel):
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Settings:
        email_collation = Collation("en", strength=2)
        indexes = [
            IndexModel("email", unique=True),
            IndexModel(
                "email", name="case_insensitive_email_index", collation=email_collation
            ),
        ]


class User(BunnetBaseUser, Document):
    pass


class BunnetBaseUserDocument(BunnetBaseUser, Document):  # type: ignore
    pass

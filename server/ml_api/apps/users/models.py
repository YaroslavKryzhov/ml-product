import uuid

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


from ml_api.common.models.base import Base


class User(SQLAlchemyBaseUserTable[UUID], Base):
    id = Column(
        UUID(as_uuid=True),
        index=True,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    #
    # __tablename__ = "user"
    #
    # id = Column(GUID, primary_key=True)
    # email = Column(String(length=320), unique=True, index=True, nullable=False)
    # hashed_password = Column(String(length=1024), nullable=False)
    # is_active = Column(Boolean, default=True, nullable=False)
    # is_superuser = Column(Boolean, default=False, nullable=False)
    # is_verified = Column(Boolean, default=False, nullable=False)

    # dataframes = relationship('DataFrame', back_populates="user")
    # models = relationship('Model', back_populates="user")

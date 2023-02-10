from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from ml_api.common.models.base import Base
from sqlalchemy.orm import relationship


class User(SQLAlchemyBaseUserTableUUID, Base):
    #
    # __tablename__ = "user"
    #
    # id = Column(GUID, primary_key=True)
    # email = Column(String(length=320), unique=True, index=True, nullable=False)
    # hashed_password = Column(String(length=1024), nullable=False)
    # is_active = Column(Boolean, default=True, nullable=False)
    # is_superuser = Column(Boolean, default=False, nullable=False)
    # is_verified = Column(Boolean, default=False, nullable=False)
    documents = relationship('Document', back_populates="user")
    models = relationship('Model', back_populates="user")

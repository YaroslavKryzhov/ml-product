from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ml_api.common.database.base_model import Base


class User(Base):
    # __table_args__ = {'extend_existing': True}
    name = Column(String)
    password = Column(String)

    documents = relationship('Document', back_populates="user")
    models = relationship('Model', back_populates="user")

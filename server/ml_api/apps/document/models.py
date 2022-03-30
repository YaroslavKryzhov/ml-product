from sqlalchemy import Column, String, DateTime,  Integer, ForeignKey, PickleType
from sqlalchemy.orm import relationship

from ml_api.common.database.base_model import Base


class Document(Base):
    __table_args__ = {'extend_existing': True}
    name = Column(String)
    filepath = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    upload_date = Column(DateTime)
    change_date = Column(DateTime)
    pipeline = Column(PickleType)

    user = relationship('User', back_populates='documents')
    used_in_models = relationship('Document', secondary='document_in_model', back_populates='used_csv')


from sqlalchemy import Column, String

from ml_api.common.database.base_model import Base


class Csv(Base):
    __table_args__ = {'extend_existing': True}
    name = Column(String)
    author = Column(String(), default='admin')

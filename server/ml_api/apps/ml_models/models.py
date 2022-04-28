import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, Table, PickleType, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from ml_api.common.database.base_model import Base


# document_in_model = Table('document_in_model', Base.metadata,
#                           Column('document_id', ForeignKey('document.id'), primary_key=True),
#                           Column('model_id', ForeignKey('model.id'), primary_key=True)
#                           )


class Model(Base):
    __tablename__ = 'model'
    # __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), index=True, primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(String)
    filepath = Column(String, unique=True)
    user_id = Column(UUID, ForeignKey("user.id"))
    csv_id = Column(UUID, ForeignKey("document.id"))
    create_date = Column(DateTime)
    task_type = Column(String)
    composition_type = Column(String)
    hyperparams = Column(PickleType)
    metrics = Column(PickleType)

    used_csv = relationship('Document', back_populates='used_in_model')
    user = relationship('User', back_populates='models')




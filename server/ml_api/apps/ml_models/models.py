import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from ml_api.common.database.base_model import Base


# document_in_model = Table('document_in_model', Base.metadata,
#                           Column('document_id', ForeignKey('document.id'), primary_key=True),
#                           Column('model_id', ForeignKey('model.id'), primary_key=True)
#                           )


class Model(Base):
    __tablename__ = 'model'

    id = Column(UUID(as_uuid=True), index=True, primary_key=True, default=uuid.uuid4, unique=True)
    name = Column(String)
    filepath = Column(String, unique=True)
    user_id = Column(UUID, ForeignKey("user.id"))
    csv_id = Column(UUID, ForeignKey("document.id"))
    features = Column(PickleType)
    target = Column(String)
    create_date = Column(DateTime)
    task_type = Column(String)
    composition_type = Column(String)
    composition_params = Column(PickleType)
    stage = Column(String)
    report = Column(PickleType)

    used_csv = relationship('Document', back_populates='used_in_model')
    user = relationship('User', back_populates='models')




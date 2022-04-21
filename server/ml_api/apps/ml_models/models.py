import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, Table, PickleType, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from ml_api.common.database.base_model import Base


document_in_model = Table('document_in_model', Base.metadata,
                          Column('document_id', ForeignKey('document.id'), primary_key=True),
                          Column('model_id', ForeignKey('model.id'), primary_key=True)
                          )


class Model(Base):
    __tablename__ = 'model'
    # __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), index=True, primary_key=True, default=uuid.uuid4)
    name = Column(String)
    filepath = Column(String, unique=True)
    user_id = Column(UUID, ForeignKey("user.id"))
    create_date = Column(DateTime)
    composition = Column(Boolean)
    # in_composition = Column(Boolean)
    hyperparams = Column(PickleType)

    used_csv = relationship('Document', secondary=document_in_model, back_populates='used_in_models')
    user = relationship('User', back_populates='models')




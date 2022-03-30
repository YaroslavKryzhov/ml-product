from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Table, PickleType
from sqlalchemy.orm import relationship

from ml_api.common.database.base_model import Base


document_in_model = Table('document_in_model', Base.metadata,
                          Column('document_id', ForeignKey('document.id'), primary_key=True),
                          Column('model_id', ForeignKey('model.id'), primary_key=True)
                          )


class Model(Base):
    # __table_args__ = {'extend_existing': True}
    name = Column(String)
    filepath = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    create_date = Column(DateTime)
    hyperparams = Column(PickleType)

    used_csv = relationship('Document', secondary=document_in_model, back_populates='used_in_models')
    user = relationship('User', back_populates='models')




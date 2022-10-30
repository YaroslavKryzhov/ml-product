import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from ml_api.common.database.base_model import Base


class Document(Base):
    __tablename__ = 'document'
    __table_args__ = {'extend_existing': True}

    id = Column(
        UUID(as_uuid=True),
        index=True,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    name = Column(String)
    filepath = Column(String, unique=True)
    user_id = Column(UUID, ForeignKey("user.id"))
    upload_date = Column(DateTime)
    change_date = Column(DateTime)
    pipeline = Column(PickleType)
    column_types = Column(PickleType)

    user = relationship('User', back_populates='documents')
    used_in_model = relationship('Model', back_populates='used_csv')

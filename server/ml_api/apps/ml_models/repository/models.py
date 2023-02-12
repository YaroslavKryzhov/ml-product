import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from ml_api.common.models.base import Base


class Model(Base):
    __tablename__ = 'model'

    id = Column(
        UUID(as_uuid=True),
        index=True,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    filename = Column(String, unique=True)
    user_id = Column(UUID, ForeignKey("user.id"))
    csv_id = Column(UUID, ForeignKey("document.id"))
    features = Column(PickleType)
    target = Column(String)
    created_at = Column(DateTime)
    task_type = Column(String)
    composition_type = Column(String)
    composition_params = Column(PickleType)
    status = Column(String)
    report = Column(PickleType)

    used_csv = relationship('Document', back_populates='used_in_model')
    user = relationship('User', back_populates='models')

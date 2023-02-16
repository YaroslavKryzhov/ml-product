import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from ml_api.common.models.base import Base
from ml_api.apps.users.models import User


class DataFrame(Base):
    __tablename__ = 'dataframe'
    __table_args__ = {'extend_existing': True}

    id = Column(
        UUID(as_uuid=True),
        index=True,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
    )
    filename = Column(String, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    pipeline = Column(PickleType)
    column_types = Column(PickleType)

    user = relationship('User')  # , back_populates='dataframes')
    # used_in_model = relationship('Model', back_populates='used_csv')

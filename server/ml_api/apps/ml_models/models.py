import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from ml_api.common.models.base import Base
from ml_api.apps.users.models import User # noqa
# from ml_api.apps.dataframes.models import DataFrame # noqa


class Model(Base):
    __tablename__ = 'model'
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
    dataframe_id = Column(UUID(as_uuid=True), ForeignKey("dataframe.id"))
    features = Column(PickleType)
    target = Column(String)
    created_at = Column(DateTime)
    task_type = Column(String)
    composition_type = Column(String)
    composition_params = Column(PickleType)
    status = Column(String)
    report = Column(PickleType)
    save_format = Column(String)

    user = relationship('User')  # , back_populates='models')
    used_csv = relationship('DataFrame')  # , back_populates='used_in_model')

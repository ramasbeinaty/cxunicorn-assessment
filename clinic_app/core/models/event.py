from .user import User
from ...db.db_setup import Base, SessionLocal

from settings import settings

from .mixins import Timestamp
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, DateTime, Float
from sqlalchemy.orm import relationship


class Event(Timestamp, Base):
    __tablename__ = settings.events_table_name

    id = Column(Integer, primary_key=True, index=True)

    created_by_user_id = Column(Integer, nullable=False)
    # created_by = relationship(User)
    event_date = Column(DateTime, default=datetime.utcnow(), nullable=False)
    event_duration_in_minutes = Column(Float, nullable=False)

    is_canceled = Column(Boolean, default=False)

    __mapper_args__ = {
        "polymorphic_identity": "event",
    }
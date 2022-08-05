from datetime import datetime
from email.policy import default

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Timestamp:
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

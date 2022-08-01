from typing import Optional
from pydantic import BaseModel

from .user import User

from ..schemas.enums import Role

from sqlalchemy import DateTime, Boolean, Column, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null

from settings import settings

class Staff(User):
    __tablename__ = settings.staff_table_name
    
    id = Column(Integer, ForeignKey(str(settings.users_table_name+".id")), primary_key=True, index=True)
    work_shift = Column(String, default="Morning Shift", nullable=False) # TODO: implement a morning and night shift system
    unavailable_days = Column(DateTime, default=None) # TODO: implement with shift system

    __mapper_args__ = {
        "polymorphic_identity": "staff",
    }
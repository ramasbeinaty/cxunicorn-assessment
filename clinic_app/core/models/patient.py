from typing import Optional
from pydantic import BaseModel

from .user import User

from sqlalchemy import DateTime, Boolean, Column, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null

from settings import settings

class Patient(User):
    __tablename__ = settings.patients_table_name
    
    id = Column(Integer, ForeignKey(str(settings.users_table_name+".id")), primary_key=True, index=True)
    medical_history = Column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "patient",
    }
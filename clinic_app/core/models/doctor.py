from typing import Optional
from pydantic import BaseModel

from .staff import Staff

from ..schemas.enums import Role

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null

from settings import settings

class Doctor(Staff):
    __tablename__ = settings.doctors_table_name
    # id = Column(Integer, primary_key=True, index=True)
    id = Column(Integer, ForeignKey(str(settings.staff_table_name+".id")), primary_key=True, index=True)
    specialization = Column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "doctor",
    }
    # profile = relationship("User", back_populates="profile")

from typing import Optional
from pydantic import BaseModel

from .staff import Staff

from ..schemas.enums import Role

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null

from settings import settings

class ClinicAdmin(Staff):
    __tablename__ = settings.clinic_admins_table_name
    # id = Column(Integer, primary_key=True, index=True)
    id = Column(Integer, ForeignKey(str(settings.staff_table_name+".id")), primary_key=True, index=True)

    __mapper_args__ = {
        "polymorphic_identity": "clinic_admin",
    }

    # profile = relationship("User", back_populates="profile")

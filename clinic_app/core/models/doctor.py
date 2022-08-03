from .staff import Staff


from sqlalchemy import Boolean, Column, ForeignKey, Integer, PrimaryKeyConstraint, String, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null

from .appointment import Appointment

from settings import settings

class Doctor(Staff):
    __tablename__ = settings.doctors_table_name
    id = Column(Integer, ForeignKey(settings.staff_table_name+".id"), primary_key=True, index=True)
    specialization = Column(String, nullable=False)
    # appointment_id = Column(Integer, ForeignKey(Appointment.id), primary_key=True)

    # create a relationship with appointments table
    # appointments=relationship("Appointment", back_populates="doctor")
    # appointments_rel=relationship("Appointment", back_populates="doctor_rel", foreign_keys="appointment.id")
    

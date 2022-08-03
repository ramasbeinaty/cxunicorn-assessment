from settings import settings

from .mixins import Timestamp
from .event import Event
from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship


class Appointment(Event):
    __tablename__ = settings.appointments_table_name

    id = Column(Integer, ForeignKey(settings.events_table_name+".id"), primary_key=True, index=True)

    # patient_id = Column(Integer, ForeignKey(settings.patients_table_name+".id"), nullable=False)
    # doctor_id = Column(Integer, ForeignKey(settings.doctors_table_name+".id"), nullable=False)

    # create a relationship with patients table
    # patient=relationship(settings.patients_table_name, back_populates="appointments")

    # create a relationship with doctors table
    # doctor_rel=relationship("Doctor", uselist=False, back_populates='appointments_rel')

    # patient = relationship(settings.patients_table_name, back_populates="patient")
    # doctor = relationship(settings.doctors_table_name, back_populates="doctor")
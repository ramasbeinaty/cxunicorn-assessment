from .enums import Role
from ..db.db_setup import Base
from settings import settings
from .mixins import Timestamp

from datetime import datetime

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship


class User(Timestamp, Base):
    __tablename__ = settings.users_table_name

    id = Column(Integer, primary_key=True, index=True)
    email_address = Column(String, unique=True, index=True, nullable=False)  
    password = Column(String, nullable=False)  

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False) 
    phone_number = Column(String, nullable=False)  

    role = Column(Enum(Role), nullable=False)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)


class Staff(User):
    __tablename__ = settings.staff_table_name

    id = Column(Integer, ForeignKey(str(settings.users_table_name + ".id")), primary_key=True, index=True)
    work_shift = Column(String, default="morning_shift", nullable=False)


class Patient(User):
    __tablename__ = settings.patients_table_name

    id = Column(Integer, ForeignKey(str(settings.users_table_name + ".id")), primary_key=True, index=True)
    medical_history = Column(String, nullable=False)

    # create a relationship with appointments table
    appointments = relationship("Appointment", back_populates="patient")


class ClinicAdmin(Staff):
    __tablename__ = settings.clinic_admins_table_name
    id = Column(Integer, ForeignKey(str(settings.staff_table_name + ".id")), primary_key=True, index=True)


class Doctor(Staff):
    __tablename__ = settings.doctors_table_name
    id = Column(Integer, ForeignKey(settings.staff_table_name + ".id"), primary_key=True, index=True)
    specialization = Column(String, nullable=False)

    # create a relationship with appointments table
    appointments = relationship("Appointment", back_populates="doctor")


class Event(Timestamp, Base):
    __tablename__ = settings.events_table_name

    id = Column(Integer, primary_key=True, index=True)

    created_by_user_id = Column(Integer, nullable=False)

    event_start_datetime = Column(DateTime, default=datetime.utcnow(), nullable=False)
    event_end_datetime = Column(DateTime, nullable=False)

    is_canceled = Column(Boolean, default=False)


class Appointment(Event):
    __tablename__ = settings.appointments_table_name

    id = Column(Integer, ForeignKey(settings.events_table_name + ".id"), primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey(settings.doctors_table_name + ".id"), primary_key=True)
    patient_id = Column(Integer, ForeignKey(settings.patients_table_name + ".id"), primary_key=True)

    # create a relationship with doctors table
    doctor = relationship("Doctor", back_populates=settings.appointments_table_name)

    # create a relationship with patients table
    patient = relationship("Patient", back_populates=settings.appointments_table_name)

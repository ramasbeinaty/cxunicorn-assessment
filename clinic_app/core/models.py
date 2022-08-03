from .enums import Role

from ..db.db_setup import Base, SessionLocal

from settings import settings

from .mixins import Timestamp

from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Float, DateTime
from sqlalchemy.orm import relationship



class User(Timestamp, Base):
    __tablename__ = settings.users_table_name

    id = Column(Integer, primary_key=True, index=True)
    email_address = Column(String, unique=True, index=True, nullable=False) # TODO: have validation for email
    password = Column(String, nullable=False) # TODO: hash the password

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=False) # TODO: change to datetime object
    phone_number = Column(String, nullable=False) # TODO: have validation for phone number

    role = Column(Enum(Role), nullable=False)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)


class Staff(User):
    __tablename__ = settings.staff_table_name
    
    id = Column(Integer, ForeignKey(str(settings.users_table_name+".id")), primary_key=True, index=True)
    work_shift = Column(String, default="Morning Shift", nullable=False) # TODO: implement a morning and night shift system
    unavailable_days = Column(DateTime, default=None) # TODO: implement with shift system and change to list of Dates


class Patient(User):
    __tablename__ = settings.patients_table_name
    
    id = Column(Integer, ForeignKey(str(settings.users_table_name+".id")), primary_key=True, index=True)
    medical_history = Column(String, nullable=False)

    # create a relationship with appointments table
    # appointments=relationship("Appointment", backref="Appointment.id", primaryjoin="Patient.id==Appointment.patient_id")
    appointments=relationship("Appointment", back_populates="patient")


class ClinicAdmin(Staff):
    __tablename__ = settings.clinic_admins_table_name
    id = Column(Integer, ForeignKey(str(settings.staff_table_name+".id")), primary_key=True, index=True)


class Doctor(Staff):
    __tablename__ = settings.doctors_table_name
    id = Column(Integer, ForeignKey(settings.staff_table_name+".id"), primary_key=True, index=True)
    specialization = Column(String, nullable=False)

    # create a relationship with appointments table
    # appointments=relationship("Appointment", backref="Appointment.id", primaryjoin="Doctor.id==Appointment.doctor_id")
    appointments=relationship("Appointment", back_populates="doctor")
    

class Event(Timestamp, Base):
    __tablename__ = settings.events_table_name

    id = Column(Integer, primary_key=True, index=True)

    created_by_user_id = Column(Integer, nullable=False)
    
    # created_by = relationship(User)
    event_date = Column(DateTime, default=datetime.utcnow(), nullable=False)
    event_duration_in_minutes = Column(Float, nullable=False)

    is_canceled = Column(Boolean, default=False)


class Appointment(Event):
    __tablename__ = settings.appointments_table_name

    id = Column(Integer, ForeignKey(settings.events_table_name+".id"), primary_key=True, index=True)

    # doctor_id = Column(Integer, ForeignKey(Doctor.id), primary_key=True)
    doctor_id = Column(Integer, ForeignKey(settings.doctors_table_name+".id"), primary_key=True)
    # patient_id = Column(Integer, ForeignKey((settings.patients_table_name).id), primary_key=True)
    patient_id = Column(Integer, ForeignKey(settings.patients_table_name+".id"), primary_key=True)

    #create a relationship with doctors table
    # doctor=relationship("Doctor", foreign_keys="Appointment.doctor_id")
    doctor=relationship("Doctor", back_populates=settings.appointments_table_name)

    # create a relationship with patients table
    # patient=relationship("Patient", foreign_keys="Appointment.patient_id")
    patient=relationship("Patient", back_populates=settings.appointments_table_name)

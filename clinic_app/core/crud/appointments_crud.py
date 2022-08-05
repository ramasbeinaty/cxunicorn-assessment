from datetime import datetime, date
from typing import List

from sqlalchemy import and_, asc, desc, func, select
from sqlalchemy.orm import Session
from clinic_app.core.crud.doctors_crud import get_doctor

from clinic_app.core.utils.appointment_handler import doctor_can_accept_appointment, get_total_appointments_by_doctor, \
    valid_appointment_dates, valid_appointment_duration

from ..models import Appointment
from ..schemas import AppointmentCreate


def get_all_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Appointment).offset(skip).limit(limit).all()


def get_all_appointments_by_day(db: Session, day: date):
    return db.query(Appointment).filter(
        Appointment.event_start_datetime >= datetime.combine(day, datetime.min.time()),
        Appointment.event_start_datetime <= datetime.combine(day, datetime.max.time()),
        Appointment.is_canceled == False
    )


def get_all_appointments_by_patient(db: Session, patient_id: int, skip: int = 0, limit: int = 100):
    return db.query(Appointment).filter(Appointment.patient_id == patient_id).offset(skip).limit(limit).all()


def get_all_appointments_by_doctor(db: Session, doctor_id: int):
    return db.query(Appointment).filter(Appointment.doctor_id == doctor_id)


def get_all_future_appointments_by_doctor_per_day(db: Session, doctor_id: int, day: date):
    return db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        and_(Appointment.event_start_datetime >= datetime.combine(day, datetime.min.time()),
             Appointment.event_end_datetime <= datetime.combine(day, datetime.max.time())),
        Appointment.is_canceled == False
    ).order_by(asc(Appointment.event_end_datetime)).all()


def get_appointment(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


def create_appointment(db: Session, appointment: AppointmentCreate):
    db_appointment = Appointment(
        doctor_id=appointment.doctor_id,
        patient_id=appointment.patient_id,
        created_by_user_id=appointment.created_by_user_id,
        is_canceled=appointment.is_canceled,
        event_start_datetime=appointment.event_start_datetime,
        event_end_datetime=appointment.event_end_datetime
    )

    # convert the appointment model to its schema
    schema_appointment = AppointmentCreate.from_orm(db_appointment)

    # check the validity of appointment start and end datetimes
    valid_appointment_dates(start_datetime=schema_appointment.event_start_datetime,
                            end_datetime=schema_appointment.event_end_datetime)

    # check appointment is of minimum and maximum duration
    valid_appointment_duration(start_datetime=schema_appointment.event_start_datetime,
                               end_datetime=schema_appointment.event_end_datetime)

    # check doctor's total appointment time in a day does not already exceed
    # or will exceed the maximum when adding this appointment
    # to do that, need to first get all current appointments of doctors in the given day
    # then compare it to the max minutes of appointments allowed in a day

    # get the appointment day
    appointment_day = schema_appointment.event_start_datetime.date()

    # get all the future (aka not past or now o'clock) appointments of doctor at given day
    db_doctor_appointments = get_all_future_appointments_by_doctor_per_day(db=db,
                                                                           doctor_id=Appointment.doctor_id,
                                                                           day=appointment_day)

    doctor_can_accept_appointment(schema_appointment, db_doctor_appointments)

    # add and commit model to db
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def cancel_appointment(db: Session, appointment: Appointment):
    setattr(appointment, "is_canceled", True)

    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def get_doctors_with_most_appointments_in_a_day(db: Session, day: date):
    return db.query(
        Appointment.doctor_id,
        func.count(Appointment.doctor_id).label("total_appointments")
    ).filter(and_(Appointment.event_start_datetime >= datetime.combine(day, datetime.min.time()),
                  Appointment.event_end_datetime <= datetime.combine(day, datetime.max.time()))
             ).group_by(Appointment.doctor_id).order_by(desc("total_appointments")).all()


def get_doctors_with_more_than_six_hours_of_appointments_in_a_day(db: Session, day: date):
    return db.query(
        Appointment.doctor_id,
        func.count(Appointment.doctor_id).label("total_appointments")
    ).filter(and_(
        Appointment.event_start_datetime >= datetime.combine(day, datetime.min.time()),
        Appointment.event_end_datetime <= datetime.combine(day, datetime.max.time()),
    )
    ).group_by(Appointment.doctor_id).having(func.count(Appointment.doctor_id) > 6
                                             ).order_by(desc("total_appointments")).all()

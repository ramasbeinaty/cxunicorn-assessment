from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from clinic_app.core.crud.patient_crud import get_patient
from clinic_app.core.utils.auth_handler import auth_wrapper
from clinic_app.core.utils.role_handler import is_clinic_admin, is_doctor_or_clinic_admin, is_patient
from clinic_app.core.schemas import Appointment, AppointmentCreate
from ...db.db_setup import get_db
from ...core.crud.appointments_crud import cancel_appointment, create_appointment, get_all_appointments, \
    get_appointment, get_all_appointments_by_patient, get_doctors_with_more_than_six_hours_of_appointments_in_a_day, \
    get_doctors_with_most_appointments_in_a_day
from ...core.crud.doctors_crud import get_doctor

from datetime import datetime

from settings import settings

router = APIRouter(dependencies=[Depends(auth_wrapper)])


@router.get("/", response_model=List[Appointment], status_code=status.HTTP_200_OK)
def read_all_appointments(skip: int=0, limit: int = 10, patient_id: int | None = None, db: Session = Depends(get_db)):
    if patient_id:
        db_appointment = get_all_appointments_by_patient(db=db, patient_id=patient_id, skip=skip, limit=limit)
    else: 
        db_appointment = get_all_appointments(db=db, skip=skip, limit=limit)

    return db_appointment


@router.get("/{appointment_id}", response_model=Appointment)
async def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    print("im in the wrong")
    db_appointment = get_appointment(db=db, appointment_id=appointment_id)
    
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No appointment with id {appointment_id} exists.")

    return db_appointment
    

@router.post("/", response_model=Appointment, status_code=status.HTTP_201_CREATED, dependencies=[Depends(is_patient)])
def create_new_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    db_doctor = get_doctor(db=db, doctor_id=appointment.doctor_id)
    db_patient = get_patient(db=db, patient_id=appointment.patient_id)

    if not db_doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No doctor with id {appointment.doctor_id} exists in the system.")
    
    if not db_patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No patient with id {appointment.patient_id} exists in the system.")

    appointment = create_appointment(db=db, appointment=appointment)
    return appointment


@router.patch("/{appointment_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(is_doctor_or_clinic_admin)])
def cancel_given_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = get_appointment(db=db, appointment_id=appointment_id)

    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No appointment with id {appointment_id} exists in the system.")

    db_cancel_appointment = cancel_appointment(db=db, appointment=db_appointment)

    return db_cancel_appointment


@router.get("/by_day/{day}", dependencies=[Depends(is_clinic_admin)])
def read_doctors_appointments_by_day(day: str, most: bool = False,
                                     above_six: bool = False, db: Session = Depends(get_db)):
    parsed_day = datetime.strptime(day, settings.date_format)

    if most:
        db_doctors = get_doctors_with_most_appointments_in_a_day(db=db, day=parsed_day)

    if above_six:
        db_doctors = get_doctors_with_more_than_six_hours_of_appointments_in_a_day(db=db, day=parsed_day)

    return db_doctors

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from clinic_app.core.crud.patient_crud import get_patient

from clinic_app.core.utils.auth_handler import auth_wrapper
from clinic_app.core.utils.role_handler import is_patient

from ...db.db_setup import get_db
from clinic_app.core.schemas import Appointment, AppointmentCreate

from ...core.crud.appointments_crud import cancel_appointment, create_appointment, get_all_appointments, get_appointment, get_all_appointments_of_patient

from ...core.crud.doctors_crud import get_doctor

import json

router = APIRouter(dependencies=[Depends(auth_wrapper)])


@router.get("/", response_model=List[Appointment], status_code=status.HTTP_200_OK)
def read_all_appointments(skip: int=0, limit: int = 10, patient_id: int | None = None, db: Session = Depends(get_db)):
    if patient_id:
        db_appointment = get_all_appointments_of_patient(db=db, patient_id=patient_id, skip=skip, limit=limit)
    else: 
        db_appointment = get_all_appointments(db=db, skip=skip, limit=limit)

    return db_appointment


@router.get("/{appointment_id}", response_model=Appointment)
async def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = get_appointment(db=db, appointment_id=appointment_id)
    
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No appointment with id {appointment_id} exists.")

    return db_appointment
    

@router.post("/", response_model=Appointment, status_code=status.HTTP_201_CREATED, dependencies=[Depends(is_patient)])
def create_new_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    db_doctor = get_doctor(db=db, doctor_id=appointment.doctor_id)
    db_patient = get_patient(db=db, patient_id=appointment.patient_id)

    if not db_doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No doctor with id {appointment.doctor_id} exists in the system.")
    
    if not db_patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No patient with id {appointment.patient_id} exists in the system.")

    appointment = create_appointment(db=db, appointment=appointment)
    return appointment

@router.patch("/{appointment_id}", status_code=status.HTTP_200_OK)
def cancel_given_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = get_appointment(db=db, appointment_id=appointment_id)

    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No appointment with id {appointment_id} exists in the system.")

    db_cancel_appointment = cancel_appointment(db=db, appointment=db_appointment)

    return db_cancel_appointment
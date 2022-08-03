from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List

from ...db.db_setup import get_db
from clinic_app.core.schemas import Appointment, AppointmentCreate, AppointmentWithDoctorAndPatientInfo

from ...core.crud.appointments_crud import create_appointment, get_all_appointments, get_appointment

router = APIRouter()

@router.get("/", response_model=List[Appointment], status_code=status.HTTP_200_OK)
def read_all_appointments(skip: int=0, limit: int = 10, db: Session = Depends(get_db)):
    appointments = get_all_appointments(db, skip=skip, limit=limit)
    return appointments

@router.get("/{appointment_id}")
async def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = get_appointment(db=db, appointment_id=appointment_id)
    
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No doctor with id {appointment_id} exists.")
    
    return db_appointment

@router.post("/", response_model=Appointment, status_code=status.HTTP_201_CREATED)
def create_new_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    appointment = create_appointment(db=db, appointment=appointment)
    return appointment
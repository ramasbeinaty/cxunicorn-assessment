from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List

from ...db.db_setup import get_db
from clinic_app.core.schemas import Doctor, DoctorCreate

from ...core.crud.doctors_crud import get_all_doctors, get_doctor, get_doctor_by_email,  create_doctor

router = APIRouter()

@router.get("/", response_model=List[Doctor])
def read_all_doctors(skip: int=0, limit: int = 10, db: Session = Depends(get_db)):
    doctors = get_all_doctors(db, skip=skip, limit=limit)
    return doctors

@router.post("/", response_model=Doctor, status_code=status.HTTP_201_CREATED)
async def create_new_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    # check if given email is already registered
    db_doctor = get_doctor_by_email(db=db, email_address=doctor.email_address)

    # if so, throw an error
    if db_doctor:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered in system.")
    
    # else return created doctor data
    return create_doctor(db=db, doctor=doctor)

@router.get("/{doctor_id}", response_model=Doctor)
async def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = get_doctor(db=db, doctor_id=doctor_id)
    if not db_doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No doctor with id {doctor_id} exists.")
    return db_doctor
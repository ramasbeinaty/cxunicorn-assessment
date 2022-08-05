from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from clinic_app.core.utils.auth_handler import auth_wrapper

from ...db.db_setup import get_db
from clinic_app.core.schemas import Doctor

from ...core.crud.doctors_crud import get_all_doctors, get_doctor

router = APIRouter(dependencies=[Depends(auth_wrapper)])


@router.get("/", response_model=List[Doctor])
def read_all_doctors(skip: int=0, limit: int = 10, db: Session = Depends(get_db)):
    doctors = get_all_doctors(db=db, skip=skip, limit=limit)
    return doctors


@router.get("/{doctor_id}", response_model=Doctor)
async def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = get_doctor(db=db, doctor_id=doctor_id)
    if not db_doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No doctor with id {doctor_id} exists.")
    return db_doctor

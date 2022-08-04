from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List

from clinic_app.core.utils.auth_handler import auth_wrapper

from ...db.db_setup import get_db
from clinic_app.core.crud.patient_crud import get_patient

router = APIRouter(dependencies=[Depends(auth_wrapper)])

# get the patient's appointment history
@router.get("/{patient_id}/appointments")
async def read_all_patient_appointments(patient_id: int, skip: int=0, limit: int = 10, db: Session = Depends(get_db)):
    db_patient = get_patient(db=db, patient_id=patient_id)
    if not db_patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No patient with id {patient_id} exists.")

    return db_patient
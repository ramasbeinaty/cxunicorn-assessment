from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from clinic_app.core.schemas.clinic_admin import ClinicAdmin, ClinicAdminFields
from clinic_app.core.schemas.user import UserCreate

from ...db.db_setup import get_db

from clinic_app.core.schemas.clinic_admin import ClinicAdmin  
from clinic_app.core.schemas.patient import Patient, PatientFields  
from clinic_app.core.schemas.doctor import Doctor, DoctorCreate, DoctorFields 

from clinic_app.core.crud.auth import register_user

from fastapi import status



router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_new_user(user_info: UserCreate, role_info: DoctorFields| PatientFields | ClinicAdminFields| None = None, db: Session = Depends(get_db)):
    return register_user(db=db, user_info= user_info, role_info=role_info)


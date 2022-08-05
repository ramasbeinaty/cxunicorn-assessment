from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from clinic_app.core.crud.doctors_crud import get_doctor_by_email

from clinic_app.core.schemas import ClinicAdmin, ClinicAdminDetails, ClinicAdminFields, DoctorDetails, PatientDetails, User, UserCreate, Patient, PatientFields, Doctor, DoctorCreate, DoctorFields, UserLogin
from clinic_app.core.utils import auth_handler
from ...db.db_setup import get_db
from clinic_app.core.crud.auth_crud import login_user, register_user

router = APIRouter()


# @router.post("/register", status_code=status.HTTP_201_CREATED, response_model=DoctorDetails| PatientDetails| ClinicAdminDetails)
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_new_user(user_info: UserCreate, role_info: DoctorFields| PatientFields | ClinicAdminFields| None = None, db: Session = Depends(get_db)):
    db_user = register_user(db=db, user_info= user_info, role_info=role_info)

    return db_user


@router.post("/login", status_code=status.HTTP_200_OK)
def sign_in_user(email_address: str, password: str, db: Session = Depends(get_db)):
    return login_user(db=db, email_address=email_address, password=password)
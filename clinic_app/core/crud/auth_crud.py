from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from clinic_app.core.schemas import ClinicAdminFields, DoctorFields, PatientFields, UserCreate

from ..schemas import Role

from ..models import User as user_model

from ..models import ClinicAdmin
from ..models import Doctor
from ..models import Patient

def get_user_by_email(db:Session, user_email: int):
    return db.query(user_model).filter(user_model.email_address == user_email).first()


def register_user(db: Session, user_info: UserCreate, role_info: DoctorFields| PatientFields| ClinicAdminFields| None = None):
    db_user = get_user_by_email(db=db, user_email=user_info.email_address)
    if db_user:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered in system.")

    try:
        if user_info.role == Role.clinic_admin:
            db_user = ClinicAdmin(
                                    work_shift = role_info.work_shift,
                                    unavailable_days = role_info.unavailable_days,
                                    email_address=user_info.email_address.lower(), 
                                    password=user_info.password,
                                    first_name = user_info.first_name.lower(),
                                    last_name=user_info.last_name.lower(),
                                    date_of_birth=user_info.date_of_birth.lower(),
                                    phone_number=user_info.phone_number,
                                    role=user_info.role
            )
        elif user_info.role == Role.doctor:
            db_user = Doctor(
                                specialization=role_info.specialization.lower(),
                                work_shift=role_info.work_shift,
                                unavailable_days=role_info.unavailable_days,
                                email_address=user_info.email_address.lower(), 
                                password=user_info.password,
                                first_name = user_info.first_name.lower(),
                                last_name=user_info.last_name.lower(),
                                date_of_birth=user_info.date_of_birth.lower(),
                                phone_number=user_info.phone_number,
                                role=user_info.role
            )
        elif user_info.role == Role.patient:
            db_user = Patient(
                                    medical_history=role_info.medical_history,
                                    email_address=user_info.email_address.lower(), 
                                    password=user_info.password,
                                    first_name = user_info.first_name.lower(),
                                    last_name=user_info.last_name.lower(),
                                    date_of_birth=user_info.date_of_birth.lower(),
                                    phone_number=user_info.phone_number,
                                    role=user_info.role
            )
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No role with name {user_info.role} exists in system.") 

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Some role info is missing -- {e}")

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

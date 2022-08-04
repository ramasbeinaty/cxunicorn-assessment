from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from clinic_app.core.crud.doctors_crud import get_doctor_by_email
from clinic_app.core.schemas import ClinicAdminFields, DoctorFields, PatientFields, UserCreate

from ..schemas import User as UserSchema

from ..schemas import HTTPResponseSchema, Role, TokenResponse
from ..models import User, ClinicAdmin, Doctor, Patient

from ..utils import auth_handler


def get_user_by_email(db:Session, email_address: str):
    return db.query(User).filter(User.email_address == email_address).first()


def register_user(db: Session, user_info: UserCreate, role_info: DoctorFields| PatientFields| ClinicAdminFields| None = None):
    db_user = get_user_by_email(db=db, email_address=user_info.email_address)
    if db_user:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered in system.")

    try:
        hashed_password = auth_handler.get_hashed_password(user_info.password)

        if user_info.role == Role.clinic_admin:
            db_user = ClinicAdmin(
                                    work_shift = role_info.work_shift,
                                    unavailable_days = role_info.unavailable_days,
                                    email_address=user_info.email_address.lower(), 
                                    password=hashed_password,
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
                                password=hashed_password,
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
                                    password=hashed_password,
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


def login_user(db: Session, email_address: str, password: str):
    db_user = get_user_by_email(db=db, email_address=email_address)

    if not db_user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not registered in system. Please register instead.")

    try:
        if not auth_handler.verify_password(password, db_user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password entered is incorrect.")

        user_schema_obj = UserSchema.from_orm(db_user)

        token = auth_handler.encode_token(data={user_schema_obj.email_address, user_schema_obj.role})
        
        return HTTPResponseSchema(status_code=status.HTTP_200_OK, message="Logged in successfully.", result=TokenResponse(access_token=token, token_type="Bearer")).dict(exclude_none=True)

    except Exception as e:
        print(e.args)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


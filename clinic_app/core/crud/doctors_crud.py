from sqlalchemy.orm import Session

from clinic_app.core.crud.appointments_crud import get_all_future_appointments_by_doctor

from ..models import Appointment, Doctor
from ..schemas import DoctorCreate

from datetime import datetime

def get_all_doctors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Doctor).offset(skip).limit(limit).all()

def get_doctor(db: Session, doctor_id: int):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()

def get_doctor_by_email(db: Session, email_address: str):
    return db.query(Doctor).filter(Doctor.email_address==email_address).first()

def create_doctor(db: Session, doctor: DoctorCreate):
    db_doctor = Doctor( specialization=doctor.specialization.lower(),
                        work_shift=doctor.work_shift,
                        unavailable_days=doctor.unavailable_days,
                        email_address=doctor.email_address.lower(), 
                        password=doctor.password,
                        first_name = doctor.first_name.lower(),
                        last_name=doctor.last_name.lower(),
                        date_of_birth=doctor.date_of_birth.lower(),
                        phone_number=doctor.phone_number,
                        role=doctor.role
                        )
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def get_available_doctor_slots(db: Session, doctor_id: int):
    future_appointments = get_all_future_appointments_by_doctor(db=db, doctor_id=doctor_id)

    

    return future_appointments



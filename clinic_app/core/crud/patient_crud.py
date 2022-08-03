from sqlalchemy.orm import Session

from ..models import Patient

def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

def get_all_patient_appointments(db: Session, patient_id: int, skip: int = 0, limit: int = 100):


    return db.query(Doctor).offset(skip).limit(limit).all()
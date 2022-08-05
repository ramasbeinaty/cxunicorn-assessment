from sqlalchemy.orm import Session

from ..models import Patient


def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()


from sqlalchemy.orm import Session

from ..models import Appointment
from ..schemas import AppointmentCreate

def get_all_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Appointment).offset(skip).limit(limit).all()

def get_appointment(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()

def create_appointment(db: Session, appointment: AppointmentCreate):
    db_appointment= Appointment( 
                            doctor_id=appointment.doctor_id,
                            created_by_user_id=appointment.created_by_user_id,
                            is_canceled=appointment.is_canceled,
                            event_date=appointment.event_date,
                            event_duration_in_minutes=appointment.event_duration_in_minutes
                        )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment
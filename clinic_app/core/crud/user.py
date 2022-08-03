from sqlalchemy.orm import Session

from ..models.user import User as user_model

def get_user_by_email(db:Session, user_email: int):
    return db.query(user_model).filter(user_model.email_address == user_email).first()

# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()
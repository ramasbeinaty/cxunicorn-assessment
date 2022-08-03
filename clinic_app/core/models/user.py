from ..schemas.enums import Role

from ...db.db_setup import Base, SessionLocal

from settings import settings

from .mixins import Timestamp

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null


class User(Timestamp, Base):
    __tablename__ = settings.users_table_name

    id = Column(Integer, primary_key=True, index=True)
    email_address = Column(String, unique=True, index=True, nullable=False) # TODO: have validation for email
    password = Column(String, nullable=False) # TODO: hash the password

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=False) # TODO: change to datetime object
    phone_number = Column(String, nullable=False) # TODO: have validation for phone number

    role = Column(Enum(Role), nullable=False)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    __mapper_args__ = {
        "polymorphic_identity": "user",
    }
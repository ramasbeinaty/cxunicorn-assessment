from datetime import datetime
from pydantic import BaseModel
from .user import UserBase, User, UserCreate

# below is used when both retrieving and creating user data
class StaffBase(UserBase):
    work_shift: str
    unavailable_days: datetime


# below includes the data needed when creating a doctor
# other fields are expected to be autogenerated
class StaffCreate(UserCreate, StaffBase):
    ...


# below is used when retrieving User
class Staff(User, StaffBase):
    id: int

    class Config:
        orm_mode = True
from datetime import datetime
from .staff import StaffBase, Staff, StaffCreate, StaffFields
from ..schemas.enums import Role

from typing import List

# required class fields without the inherited fields
class DoctorFields(StaffFields):
    specialization: str


# below is used when both retrieving and creating doctor data
class DoctorBase(StaffBase, DoctorFields):
    ...

class DoctorCreate(StaffCreate, DoctorBase):
    # role: int = Role.doctor.value
    role: str = Role.doctor.value
    ...
    

# below is used when retrieving Doctor
class Doctor(Staff, DoctorBase):
    id: int

    # booked_appointments: List[Appointment] = []

    class Config:
        orm_mode = True
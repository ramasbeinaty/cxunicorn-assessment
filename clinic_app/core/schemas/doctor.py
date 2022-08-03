from datetime import datetime
from .staff import StaffBase, Staff, StaffCreate
from ..schemas.enums import Role

from typing import List

# below is used when both retrieving and creating doctor data
class DoctorBase(StaffBase):
    specialization: str


class DoctorCreate(StaffCreate, DoctorBase):
    # role: int = Role.doctor.value
    role: str = Role.doctor.value
    ...
    

# below is used when retrieving Doctor
class Doctor(Staff, DoctorBase):
    id: int

    # appointments_rel: List[Appointment] = []

    class Config:
        orm_mode = True
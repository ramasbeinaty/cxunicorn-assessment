from .staff import StaffBase, Staff, StaffCreate, StaffFields
from ..schemas.enums import Role

from typing import List

# required class fields without the inherited fields
class ClinicAdminFields(StaffFields):
    ...


# below is used when both retrieving and creating doctor data
class ClinicAdminBase(StaffBase):
    ...


class ClinicAdminCreate(StaffCreate, ClinicAdminBase):
    # role: int = Role.doctor.value
    role: str = Role.clinic_admin.value
    ...
    

# below is used when retrieving Doctor
class ClinicAdmin(Staff, ClinicAdminBase):
    id: int

    # booked_appointments: List[Appointment] = []

    class Config:
        orm_mode = True
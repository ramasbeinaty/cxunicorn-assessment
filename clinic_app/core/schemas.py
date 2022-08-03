from datetime import datetime
from pydantic import BaseModel
from .enums import Role


"""
    USER SCHEMA
"""
# below is used when both retrieving and creating user data
class UserBase(BaseModel):
    email_address: str
    first_name: str
    last_name: str
    date_of_birth: str # TODO: change to datetime object
    phone_number: str # TODO: have validation
    role: str


# below includes the data needed when creating a user
# other fields are expected to be autogenerated
class UserCreate(UserBase):
    password: str


# below is used when retrieving User
class User(UserBase):
    id: int
    
    created_at: datetime
    is_active: bool
    is_verified: bool

    class Config:
        orm_mode = True


"""
    PATIENT SCHEMA
"""

# required class fields without the inherited fields
class PatientFields(BaseModel):
    medical_history: str

# below is used when both retrieving and creating user data
class PatientBase(UserBase, PatientFields):
    ...


# below includes the data needed when creating a doctor
# other fields are expected to be autogenerated
class PatientCreate(UserCreate, PatientBase):
    role: str = Role.patient.value
    ...


# below is used when retrieving User
class Patient(User, PatientBase):
    id: int

    # appointments: List[Appointment] = []

    class Config:
        orm_mode = True


"""
    STAFF SCHEMA
"""
# required class fields without the inherited fields
class StaffFields(BaseModel):
    work_shift: str
    unavailable_days: datetime

# below is used when both retrieving and creating user data
class StaffBase(UserBase, StaffFields):
    ...


# below includes the data needed when creating a doctor
# other fields are expected to be autogenerated
class StaffCreate(UserCreate, StaffBase):
    ...


# below is used when retrieving User
class Staff(User, StaffBase):
    id: int

    class Config:
        orm_mode = True


"""
    CLINIC ADMIN SCHEMA
"""

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


"""
    DOCTOR SCHEMA
"""
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


"""
    EVENT SCHEMA
"""

# below is used when both retrieving and creating user data
class EventBase(BaseModel):
    created_by_user_id: int
    is_canceled: bool = False
    event_date: datetime
    event_duration_in_minutes: float


# below includes the data needed when creating a user
# other fields are expected to be autogenerated
class EventCreate(EventBase):
    ...


# below is used when retrieving User
class Event(EventBase):
    id: int

    class Config:
        orm_mode = True

"""
    APPOINTMENT SCHEMA
"""
# below is used when both retrieving and creating user data
class AppointmentBase(EventBase):
    doctor_id: int
    patient_id: int
    ...


# below includes the data needed when creating a user
# other fields are expected to be autogenerated
class AppointmentCreate(EventCreate, AppointmentBase):
    ...


# below is used when retrieving User
class Appointment(Event, AppointmentBase):
    id: int

    class Config:
        orm_mode = True
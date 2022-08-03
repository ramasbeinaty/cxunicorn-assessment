from enum import Enum

class Role(str, Enum):
    clinic_admin = "clinic_admin"
    doctor = "doctor"
    patient = "patient"
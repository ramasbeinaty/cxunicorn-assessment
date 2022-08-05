from enum import Enum


class Role(str, Enum):
    clinic_admin = "clinic_admin"
    doctor = "doctor"
    patient = "patient"


class Shift(str, Enum):
    morning_shift = "morning_shift"
    night_shift = "night_shift"

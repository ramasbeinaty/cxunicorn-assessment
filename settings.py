from pydantic import BaseSettings
from decouple import config

class Settings(BaseSettings):
    app_name: str = "Clinic API"

    doctors_str: str = "doctors"
    patients_str: str = "patients"
    clinic_admins_str: str = "clinic_admins"
    users_str: str = "users"
    staff_str: str = "staffs"
    events_str: str = "events"
    appointments_str: str = "appointments"
    auth_str: str = "auth"

    # endpoint prefixes
    api_endpoint: str = "/api"
    auth_endpoint: str = "/" + auth_str
    doctors_endpoint: str = "/" + doctors_str
    patients_endpoint: str = "/" + patients_str
    appointments_endpoint: str = "/" + appointments_str
    
    # database tables
    doctors_table_name = doctors_str
    patients_table_name = patients_str
    users_table_name = users_str
    clinic_admins_table_name = clinic_admins_str
    staff_table_name = staff_str
    events_table_name = events_str
    appointments_table_name = appointments_str

    # Doctor Appointments Rules
    doctor_max_appointments_per_day = 12
    doctor_max_total_appointments_minutes_per_day = 480
    min_appointment_duration_in_minutes = 15
    max_appointment_duration_in_minutes = 120

    # JWT Configuration
    SECRET_KEY = config("SECRET_KEY")
    ALGORITHM = config("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))

    
settings = Settings()
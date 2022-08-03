from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Clinic API"

    doctors_str: str = "doctors"
    patients_str: str = "patients"
    clinic_admins_str: str = "clinic_admins"
    users_str: str = "users"
    staff_str: str = "staffs"
    events_str: str = "events"
    appointments_str: str = "appointments"

    # endpoint prefixes
    api_endpoint: str = "/api"
    auth_endpoint: str = "/auth"
    doctors_endpoint: str = "/" + doctors_str
    patients_endpoint: str = "/" + patients_str
    
    # database tables
    doctors_table_name = doctors_str
    patients_table_name = patients_str
    users_table_name = users_str
    clinic_admins_table_name = clinic_admins_str
    staff_table_name = staff_str
    events_table_name = events_str
    appointments_table_name = appointments_str


    
    class Config:
        env_file = ".env"

settings = Settings()
from functools import lru_cache

from fastapi import FastAPI, Depends

from clinic_app.api.api import api_router

from clinic_app.db.db_setup import engine, Base
from clinic_app.core.models import clinic_admin, user, doctor, patient, appointment, event

from settings import settings

# create the tables in db
# user.Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)
# doctor.Base.metadata.create_all(bind=engine)
# patient.Base.metadata.create_all(bind=engine)
# clinic_admin.Base.metadata.create_all(bind=engine)

# doctor1 = doctor.Doctor()
# appointment1 = appointment.Appointment()

# doctor1.appointments

app = FastAPI(title=settings.app_name)

app.include_router(api_router)
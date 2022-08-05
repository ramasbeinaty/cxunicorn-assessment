from clinic_app.api.api import api_router
from clinic_app.db.db_setup import engine, Base

from fastapi import FastAPI
from settings import settings

# create the tables in db
Base.metadata.create_all(bind=engine)

# create the app
app = FastAPI(title=settings.app_name)

# add the endpoints to the app
app.include_router(api_router)

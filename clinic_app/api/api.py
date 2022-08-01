from fastapi import APIRouter

from clinic_app.api.endpoints import doctors

from settings import settings

api_router = APIRouter(prefix=settings.api_endpoint, tags=[settings.doctors_str])
api_router.include_router(doctors.router, prefix=settings.doctors_endpoint)

@api_router.get("/", status_code=200)
def get_all_doctors(): 
    return {"message": "Hello World"}
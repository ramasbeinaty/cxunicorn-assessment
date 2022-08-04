from fastapi import APIRouter

from clinic_app.api.endpoints import appointments, doctors, auth

from settings import settings

api_router = APIRouter(prefix=settings.api_endpoint)
api_router.include_router(auth.router, prefix=settings.auth_endpoint, tags=[settings.auth_str])
api_router.include_router(doctors.router, prefix=settings.doctors_endpoint, tags=[settings.doctors_str])
api_router.include_router(appointments.router, prefix=settings.appointments_endpoint, tags=[settings.appointments_str])

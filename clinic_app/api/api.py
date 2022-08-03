from fastapi import APIRouter

from clinic_app.api.endpoints import doctors, auth

from settings import settings

api_router = APIRouter(prefix=settings.api_endpoint, tags=[settings.doctors_str])
api_router.include_router(auth.router, prefix=settings.auth_endpoint)
api_router.include_router(doctors.router, prefix=settings.doctors_endpoint)

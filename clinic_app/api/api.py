from fastapi import APIRouter

from api.endpoints import doctors

api_router = APIRouter(prefix="/api")
api_router.include_router(doctors.router, prefix="/doctors", tags=["doctors"])
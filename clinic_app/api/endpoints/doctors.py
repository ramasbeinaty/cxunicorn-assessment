from fastapi import APIRouter

from clinic_app.core.models.doctor import Doctor

router = APIRouter()

@router.get("/", status_code=201)
def get_all_doctors():
    return {"message": "Hello Doctors!"}
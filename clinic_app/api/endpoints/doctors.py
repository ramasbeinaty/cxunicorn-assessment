from fastapi import APIRouter

from core.models.doctors import Doctor

router = APIRouter()

@router.get("/", status_code=201)
def get_all_doctors():
    return {"message": "Hello World"}


from fastapi import Depends, HTTPException, status
from clinic_app.core.enums import Role
from clinic_app.core.utils.auth_handler import auth_wrapper



def is_patient(claims: dict = Depends(auth_wrapper)):
    role = claims.get("role")

    if role != Role.patient:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Logged user is not authorized to access this endpoint.")

    return claims




from typing import Optional
from pydantic import BaseModel
from core.schemas.enums import Role

class Doctor(BaseModel):
    id: Optional[int] = 1
    name: str
    role: Role
    # specialization: str
    # work_shift: str
    # unavailable_days: 

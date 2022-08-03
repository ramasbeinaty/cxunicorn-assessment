from datetime import datetime
from pydantic import BaseModel


# below is used when both retrieving and creating user data
class UserBase(BaseModel):
    email_address: str
    first_name: str
    last_name: str
    date_of_birth: str # TODO: change to datetime object
    phone_number: str # TODO: have validation
    role: str


# below includes the data needed when creating a user
# other fields are expected to be autogenerated
class UserCreate(UserBase):
    password: str


# below is used when retrieving User
class User(UserBase):
    id: int
    
    created_at: datetime
    is_active: bool
    is_verified: bool

    class Config:
        orm_mode = True
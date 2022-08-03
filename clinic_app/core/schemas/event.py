from datetime import datetime
from pydantic import BaseModel

# below is used when both retrieving and creating user data
class EventBase(BaseModel):
    created_by_user_id: int
    is_canceled: bool = False
    event_date: datetime
    event_duration_in_minutes: float


# below includes the data needed when creating a user
# other fields are expected to be autogenerated
class EventCreate(EventBase):
    ...


# below is used when retrieving User
class Event(EventBase):
    id: int

    class Config:
        orm_mode = True
from typing import List
from uuid import UUID, uuid1
from models_example import User, Gender, Role

from fastapi import FastAPI, HTTPException

app = FastAPI()

db: List[User] = [
    User(id=UUID("be194c6d-5d45-43a3-8477-3b4d79ab0e89"), 
    first_name="John", 
    last_name="Doe",
    gender=Gender.female,
    roles=[Role.student]
    ),
    User(id=UUID("5e5954ad-dbb9-49c5-a5d4-4b295d097728"), 
    first_name="admin", 
    last_name="admin",
    gender=Gender.male,
    roles=[Role.admin, Role.user]
    )
]

# HOME
@app.get("/")
def read_root():
    return {"Hello": "World"}

# LIST USERS
@app.get("/api/users")
async def fetch_all_users():
    return db

@app.get("/api/users/{user_id}")
async def fetch_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            return user

# ADD A USER
@app.post("/api/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

# DELETE A USER
@app.delete("/api/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f'user with id: {user_id} does not exist'
    )

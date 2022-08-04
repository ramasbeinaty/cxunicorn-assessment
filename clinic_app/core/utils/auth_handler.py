from datetime import datetime, timedelta
from typing import Optional
import jwt
import json

from settings import settings

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Security, status

from passlib.context import CryptContext

# encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer()

# encode/decode token
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

def get_hashed_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def encode_token(user_principal, user_role, expire_timedelta: Optional[timedelta]=None):

    if expire_timedelta:
        expire = datetime.utcnow() + expire_timedelta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "exp": expire,
        "lat": datetime.utcnow().timestamp(),
        "sub": user_principal,
        "role": user_role
    }

    encoded_jwt = jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        return payload if payload["exp"] >= datetime.utcnow().timestamp() else None
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token signature expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid.")

# dependency injection wrapper for auth
# ensures that the token is present, then decodes it
def auth_wrapper(auth: HTTPAuthorizationCredentials=Security(security)):
    return decode_token(auth.credentials)
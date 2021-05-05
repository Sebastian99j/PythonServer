from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from passlib.context import CryptContext
import bcrypt


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return payload
    except Exception:
        raise HTTPException(status_code=404, detail="not found")


def get_password_hash(password):
    hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    return hashed


def get_password_check(password, hashed):
    is_check = bcrypt.checkpw(password.encode('utf8'), hashed)
    return is_check

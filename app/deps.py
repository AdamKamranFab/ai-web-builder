from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from typing import Optional
from jose import jwt
from app.settings import settings
from datetime import datetime, timedelta


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/login', auto_error=False)


class TokenData(BaseModel):
    user_id: Optional[int]
    email: Optional[EmailStr]


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def sign_jwt(payload: dict):
    return jwt.encode(payload, settings.secret_key, settings.secret_algorithm)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, settings.secret_key, algorithms=[settings.secret_algorithm])
        print(decoded_token, "Decoded Token")

        return decoded_token
    except BaseException as e:
        raise e


def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.secret_algorithm])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return None


def create_access_token(user):
    expiry_time = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": expiry_time
    }
    return sign_jwt(payload)

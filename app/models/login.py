from app.deps import verify_password, create_access_token
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.models.users import UserBase
from fastapi import HTTPException, status
from typing import Dict


class LoginModel(BaseModel):
    email: EmailStr
    password: str

    def login(self, db: Session):
        user = UserBase.get_user_by_email(self.email, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!')

        pwd_verified = verify_password(self.password, user.password)
        if not pwd_verified:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

        tokens = LoginModel.generate_token(user)
        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone
        }
        return {
            **tokens,
            **user_data
        }

    @staticmethod
    def generate_token(user) -> Dict:
        access_token = create_access_token(user)
        refresh_token = create_access_token(user)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

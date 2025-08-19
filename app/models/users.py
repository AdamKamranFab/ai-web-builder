from app.database.tables import Users
from sqlalchemy.orm import Session
from app.deps import hash_password
from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.email_sender import send_verification_email, generate_otp
from fastapi import HTTPException
from app.deps import verify_password


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: str

    @staticmethod
    def get_user_by_email(email: str, db: Session):
        return db.query(Users).filter(
            Users.email == email
        ).first()


class UserSignup(UserBase):
    password: str

    def signup(self, db: Session):
        otp = generate_otp(6)
        self.password = hash_password(self.password)

        new_user = Users(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            phone=self.phone,
            otp=otp
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        send_verification_email(self.email, otp)

        return {"message": "new user created successfully!"}


class UserResponse(UserBase):
    id: int
    joined_on: datetime

    class Config:
        orm_mode = True


class ResetPassword(BaseModel):
    email: EmailStr
    pwd_old: str
    pwd_new: str

    def reset_pwd(self, db: Session):
        user = UserBase.get_user_by_email(self.email, db)

        if not user:
            raise HTTPException(status_code=404, detail='User not found')

        if not verify_password(self.pwd_old, user.password):
            raise HTTPException(status_code=403, detail='Old password is incorrect')

        if self.pwd_new == self.pwd_old:
            raise HTTPException(status_code=409, detail='New password is same as old password')

        hashed_new_pwd = hash_password(self.pwd_new)
        user.password = hashed_new_pwd
        db.commit()

        return {
            "message": "password reset successfully!"
        }

    @staticmethod
    def send_resend_pass_email(email: str, db: Session):
        otp = generate_otp(6)
        send_verification_email(email, otp)

        current = UserBase.get_user_by_email(email, db)

        current.otp = otp
        db.commit()

        return {
            "message": "Password reset email sent!"
        }

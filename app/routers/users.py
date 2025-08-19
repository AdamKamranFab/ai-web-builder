from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.users import UserSignup, ResetPassword
from app.models.login import LoginModel
from app.database.config import get_session
from app.models.email_sender import verify_otp_from_mail, verify_otp_for_reset

users = APIRouter(tags=['Users'], prefix='/user')


@users.post('/signup')
async def signup(
        payload: UserSignup,
        db: Session = Depends(get_session)
):
    try:
        return payload.signup(db)
    except BaseException as e:
        raise e


@users.post('/login')
async def login(
        payload: LoginModel,
        db: Session = Depends(get_session)
):
    try:
        return payload.login(db)
    except BaseException as e:
        return e


@users.get('/verify-token')
async def verify_otp(
        otp: str,
        db: Session = Depends(get_session)
):
    try:
        return verify_otp_from_mail(otp, db)
    except BaseException as e:
        raise e


@users.post('/send-reset-password-email')
async def resent_pwd_mail(
        email: str,
        db: Session = Depends(get_session)
):
    try:
        return ResetPassword.send_resend_pass_email(email, db)
    except BaseException as e:
        raise e


@users.patch('/reset-password')
async def reset_pwd(
        payload: ResetPassword,
        db: Session = Depends(get_session)
):
    try:
        return payload.reset_pwd(db)
    except BaseException as e:
        raise e


@users.get('/verify-reset-otp')
async def reset_otp_verify(
        otp: str,
        db: Session = Depends(get_session)
):
    try:
        return verify_otp_for_reset(otp, db)
    except BaseException as e:
        raise e

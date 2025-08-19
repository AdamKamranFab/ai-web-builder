import smtplib
import random
import string
from app.settings import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.tables import Users


def generate_otp(length: int = 6) -> str:
    return ''.join(random.choices(string.digits, k=length))


def send_verification_email(email: str, otp: str):
    try:
        message = MIMEMultipart()
        message["From"] = settings.smtp_email_address
        message["To"] = email
        message["Subject"] = "Your Verification Code"

        plain_text = f"Your verification code is: {otp}. It will expire in 10 minutes."

        body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2>Email Verification</h2>
            <p>Please use the following code to verify your email address:</p>
            <p style="font-size: 24px; font-weight: bold; letter-spacing: 4px; color: #2a9d8f;">
                {otp}
            </p>
            <p>This code will expire in 10 minutes.</p>
          </body>
        </html>
        """

        message.attach(MIMEText(plain_text, "plain"))
        message.attach(MIMEText(body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(settings.smtp_email_address, settings.smtp_email_password)
            smtp.sendmail(settings.smtp_email_address, email, message.as_string())

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


def verify_otp_from_mail(otp: str, db: Session):
    otp_current = bool(db.query(Users).filter(
        Users.otp == otp
    ).first())

    return otp_current


def send_password_reset_email(email: str, otp: str):
    try:
        message = MIMEMultipart()
        message["From"] = settings.smtp_email_address
        message["To"] = email
        message["Subject"] = "Your Password Reset Code"

        plain_text = f"Your password reset code is: {otp}. It will expire in 10 minutes."

        body = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2>Password Reset Request</h2>
            <p>We received a request to reset your password. Please use the following code to proceed:</p>
            <p style="font-size: 24px; font-weight: bold; letter-spacing: 4px; color: #e76f51;">
                {otp} </p> <p>This code will expire in 10 minutes. If you did not request a password reset, 
                please ignore this email.</p> </body> </html>"""

        message.attach(MIMEText(plain_text, "plain"))
        message.attach(MIMEText(body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(settings.smtp_email_address, settings.smtp_email_password)
            smtp.sendmail(settings.smtp_email_address, email, message.as_string())

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send password reset email: {str(e)}")


def verify_otp_for_reset(otp: str, db: Session):
    return bool(
        db.query(Users).filter(
            Users.otp == otp
        ).first()
    )

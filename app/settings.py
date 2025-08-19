from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class AppSettings(BaseSettings):
    secret_key: str = Field(..., env='SECRET_KEY')
    secret_algorithm: str = Field(..., env='SECRET_ALGORITHM')
    access_token_expire_minutes: int = Field(..., env='ACCESS_TOKEN_EXPIRE_MINUTES')
    smtp_email_address: str = Field(..., env='SMTP_EMAIL_ADDRESS')
    smtp_email_password: str = Field(..., env='SMTP_EMAIL_PASSWORD')


settings = AppSettings()

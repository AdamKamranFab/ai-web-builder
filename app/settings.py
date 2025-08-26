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
    postgres_db: str = Field(..., env='POSTGRES_DB')
    postgres_password: str = Field(..., env='POSTGRES_PASSWORD')
    google_client_id: str = Field(..., env='GOOGLE_CLIENT_ID')
    google_client_secret: str = Field(..., env='GOOGLE_CLIENT_SECRET')
    front_end_live_url: str = Field(..., env='FRONT_END_LIVE_URL')
    stripe_secret_key: str = Field(..., env='STRIPE_SECRET_KEY')
    stripe_publishable_key: str = Field(..., env='STRIPE_PUBLISHABLE_KEY')


settings = AppSettings()

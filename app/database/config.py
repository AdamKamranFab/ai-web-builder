from contextlib import contextmanager
from pydantic import Field
from pydantic_settings import BaseSettings
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    database_url: str = Field(env="DATABASE_URL")
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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_engine(self):
        try:
            assert self.database_url, "DATABASE_URL is not set"
            return create_engine(self.database_url, pool_size=20, max_overflow=30)
        except AssertionError as a_error:
            print(a_error)
        return None

    @staticmethod
    def get_session(db_engine):
        return scoped_session(
            sessionmaker(autoflush=False, bind=db_engine)
        )


settings = Settings()
engine = settings.get_engine()


@contextmanager
def get_session_ctx():
    db_session = Settings.get_session(db_engine=engine)
    db = db_session()
    print("Session created")
    try:
        yield db
    finally:
        db.close()
        db_session.remove()
        print("Session closed and removed")


def get_session():
    with get_session_ctx() as db:
        yield db

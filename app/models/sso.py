from starlette.config import Config
from authlib.integrations.starlette_client import OAuth
from app.settings import settings
from fastapi.requests import Request
from app.models.users import UserSignup, UserBase
from app.models.login import LoginModel
from sqlalchemy.orm import Session
from app.database.tables import Users


class GoogleOAuth:
    def __init__(self):
        config = Config(".env")
        self.oauth = OAuth(config)
        self.oauth.register(
            name='google',
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
            access_token_url='https://oauth2.googleapis.com/token',
            authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
            api_base_url='https://www.googleapis.com/oauth2/v2/',
            userinfo_endpoint='https://www.googleapis.com/oauth2/v2/userinfo',
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={'scope': 'openid email profile'},
        )

    async def get_authorize_redirect(self, request: Request):
        redirect_uri = 'http://127.0.0.1:8005/auth/google/callback'
        return await self.oauth.google.authorize_redirect(request, redirect_uri)

    async def get_token(self, request: Request):
        return await self.oauth.google.authorize_access_token(request)

    async def get_user_info(self, token: dict):
        resp = await self.oauth.google.get("userinfo", token=token)
        return resp.json()

    @staticmethod
    def create_user_after_callback(payload: UserSignup, db: Session):
        current_user = UserBase.get_user_by_email(payload.email, db)
        if current_user:
            application_user = current_user
            tokens = LoginModel.generate_token(application_user)
            return {
                **tokens
            }

        application_user = payload.signup(db)
        tokens = LoginModel.generate_token(application_user)

        return {
            **tokens
        }

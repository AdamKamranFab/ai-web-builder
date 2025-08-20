import urllib.parse
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from app.models.sso import GoogleOAuth
from sqlalchemy.orm import Session
from app.database.config import get_session
from app.settings import settings
from app.models.users import UserSignup

sso_router = APIRouter(tags=['SSO'], prefix='/auth')


@sso_router.get('/google/login')
async def auth_google(
        request: Request
):
    try:
        google_auth = GoogleOAuth()
        return await google_auth.get_authorize_redirect(request)
    except BaseException as e:
        raise e


@sso_router.get('/google/callback')
async def callback_google(
        request: Request,
        db: Session = Depends(get_session)
):
    try:
        google_oauth = GoogleOAuth()
        token = await google_oauth.get_token(request)
        user = await google_oauth.get_user_info(token)

        payload = UserSignup(
            email=user.get('email'),
            first_name=user.get('given_name') if user.get('given_name') else '',
            last_name=user.get('family_name') if user.get('family_name') else '',
            phone='',
            password='sso-pass'
        )
        application_user = GoogleOAuth.create_user_after_callback(payload, db)

        query_params = {
            "token": application_user.get('access_token')
        }

        redirect_url = f"{settings.front_end_live_url}/auth/google/sso-verify?{urllib.parse.urlencode(query_params)}"

        return RedirectResponse(url=redirect_url)

    except BaseException as e:
        raise e

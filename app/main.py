from fastapi import FastAPI
from app.routers.users import users
from app.routers.sso import sso_router
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings
from starlette.middleware.sessions import SessionMiddleware
from app.routers.stripe import stripe_router


app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    https_only=True,
    same_site="none"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users)
app.include_router(sso_router)
app.include_router(stripe_router)



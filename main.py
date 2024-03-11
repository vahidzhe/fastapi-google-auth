from fastapi import FastAPI
from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.requests_client import OAuth2Session

from authlib.integrations.starlette_client import OAuth
from pprint import pprint

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")


config = Config('.env')
oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.get("/login/google")
async def login_google(request: Request):
    redirect_uri = request.url_for('auth_google')
    google = oauth.create_client('google')
    response = await google.authorize_redirect(request, redirect_uri)
    return  {"url": response.headers["location"]}


@app.get("/auth")
async def auth_google(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token['userinfo']
    return user
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates

from app.api.routes import router

load_dotenv()

app = FastAPI(title="Instand Chords")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY")
)

templates = Jinja2Templates(directory="app/templates")
app.state.templates = templates

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)

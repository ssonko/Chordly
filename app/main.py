# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.api.routes import router
import os

app = FastAPI(title="Instant Chords")

app.add_middleware(
    SessionMiddleware,
    secret_key="dev-secret-key"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)

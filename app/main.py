from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import router

app = FastAPI(title="Chordly")

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include all page + API routes
app.include_router(router)

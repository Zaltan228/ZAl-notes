from fastapi import FastAPI

from backend.routers import notes

app = FastAPI(
    title="ZAl Notes",
    description="A simple API used for the notes application",
    version="1.0.0"
)

app.include_router(notes.router)
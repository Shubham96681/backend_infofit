import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes.tickets import router as tickets_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ticket Desk API")

DEFAULT_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

extra_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=DEFAULT_ORIGINS + extra_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tickets_router)


@app.api_route("/", methods=["GET", "HEAD"])
def home():
    return {"message": "Ticket Desk API is running"}


@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok"}

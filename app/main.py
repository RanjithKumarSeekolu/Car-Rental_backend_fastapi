from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from app.core.config import settings    
from app.core.exceptions import register_exception_handlers 
from app.api.deps import CurrentUser
from app.api.v1.router import api_router

app = FastAPI(title="RentNHost API")

register_exception_handlers(app)

ALLOWED_ORIGINS = [
    "http://localhost:1234",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]

extra_origins = [o.strip() for o in settings.cors_origin.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS + extra_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=PlainTextResponse)
def root():
    return "Car Rental"

# Health check endpoint
@app.get("/health")
def health():
    return {"ok": True}

@app.get("/api/me")
def me(user: CurrentUser):
    return user

app.include_router(api_router, prefix="/api")
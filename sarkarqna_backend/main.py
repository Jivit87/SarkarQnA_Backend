# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import scheme_router
from config import settings
from core.utils.logger import logger

app = FastAPI(
    title="SarkarQnA Backend",
    description="AI Bot for Government Scheme Eligibility",
    version="1.0.0"
)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(scheme_router.router, prefix="/api", tags=["Schemes"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to SarkarQnA AI Backend!",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "SarkarQnA Backend",
        "version": "1.0.0"
    }
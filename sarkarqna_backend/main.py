# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from api import scheme_router
from config import settings
from core.utils.logger import logger
from socket_handlers import sio

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

# Mount Socket.IO app
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)
app = socket_app

# Include router
app.include_router(scheme_router.router, prefix="/api", tags=["Schemes"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to SarkarQnA AI Backend!",
        "version": "1.0.0",
        "docs": "/docs",
        "socket": "/socket.io/"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "SarkarQnA Backend",
        "version": "1.0.0",
        "socket_available": True
    }

@app.get("/socket-status")
async def socket_status():
    """Check Socket.IO server status"""
    return {
        "socket_io": "running",
        "endpoint": "/socket.io/",
        "events": [
            "connect", "disconnect", "message", "chat_message", 
            "send_message", "response", "error", "message_ack",
            "ping", "pong", "get_status", "status"
        ]
    }
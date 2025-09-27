# config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    HUGGINGFACE_API_TOKEN: str = os.getenv("HUGGINGFACE_API_TOKEN", "")
    LANGGRAPH_API_KEY: str = os.getenv("LANGGRAPH_API_KEY", "")
    
    # HuggingFace Model Settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "microsoft/DialoGPT-medium")
    
    # Device Settings
    DEVICE: str = os.getenv("DEVICE", "cpu")  # cpu, cuda, auto
    USE_LOCAL_MODEL: bool = os.getenv("USE_LOCAL_MODEL", "true").lower() == "true"
    
    # Paths
    EMBEDDING_PATH: str = os.getenv("EMBEDDING_PATH", "data/embeddings")
    SCHEMES_PDF_PATH: str = os.getenv("SCHEMES_PDF_PATH", "data/schemes_pdf")
    
    # API Settings
    MAX_RETRIEVAL_DOCS: int = int(os.getenv("MAX_RETRIEVAL_DOCS", "3"))
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))
    
    # HuggingFace Model Settings
    MAX_LENGTH: int = int(os.getenv("MAX_LENGTH", "512"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.1"))
    DO_SAMPLE: bool = os.getenv("DO_SAMPLE", "true").lower() == "true"
    
    # CORS Settings
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",  # Vite's default port
        "http://127.0.0.1:5173",
        "http://localhost",
        "*"
    ]
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Development Settings
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    ENABLE_LANGGRAPH: bool = os.getenv("ENABLE_LANGGRAPH", "true").lower() == "true"

settings = Settings()

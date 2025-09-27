# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    HUGGINGFACE_API_TOKEN: str = os.getenv("HUGGINGFACE_API_TOKEN", "")
    LANGGRAPH_API_KEY: str = os.getenv("LANGGRAPH_API_KEY", "")
    
    # Model Settings
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    
    # Paths
    EMBEDDING_PATH: str = os.getenv("EMBEDDING_PATH", "data/embeddings")
    SCHEMES_PDF_PATH: str = os.getenv("SCHEMES_PDF_PATH", "data/schemes_pdf")
    
    # API Settings
    MAX_RETRIEVAL_DOCS: int = int(os.getenv("MAX_RETRIEVAL_DOCS", "3"))
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))
    
    # CORS Settings
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost",
        "*"
    ]

settings = Settings()

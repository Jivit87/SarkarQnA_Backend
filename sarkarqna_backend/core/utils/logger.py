# app/utils/logger.py

import logging
import sys
from datetime import datetime

def setup_logger(name: str = "sarkarqna", level: str = "INFO") -> logging.Logger:
    """
    Setup logger with consistent formatting
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def log_query(query: str, response: dict, user_id: str = None):
    """
    Log query and response for analytics
    """
    logger = setup_logger("query_analytics")
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "eligible": response.get("eligible", False),
        "confidence": response.get("confidence", 0.0),
        "user_id": user_id
    }
    logger.info(f"Query processed: {log_data}")

# Global logger instance
logger = setup_logger()

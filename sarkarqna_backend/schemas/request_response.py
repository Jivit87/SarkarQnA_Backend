# schemas/request_response.py

from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    query: str
    language: str = "hi"

class QueryResponse(BaseModel):
    eligible: bool
    reason: str
    confidence: float
    sources: List[str]


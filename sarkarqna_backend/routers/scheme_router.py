# app/routers/scheme_router.py

from fastapi import APIRouter, HTTPException
from schemas.request_response import QueryRequest, QueryResponse
from core.services.rag_service import RAGService
from core.services.langgraph_service import LangGraphService
from config import settings
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
try:
    rag_service = RAGService(embedding_path=settings.EMBEDDING_PATH)
    langgraph_service = LangGraphService(api_key=settings.LANGGRAPH_API_KEY)
    logger.info("Services initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize services: {e}")
    rag_service = None
    langgraph_service = None

@router.post("/check-eligibility", response_model=QueryResponse)
async def check_eligibility(request: QueryRequest):
    """
    Main endpoint:
    - Accepts Hindi/Hinglish queries
    - Returns eligibility, reason, confidence, and sources
    """
    try:
        # Validate services are available
        if not rag_service:
            raise HTTPException(status_code=503, detail="RAG service not available")
        
        # 1️⃣ Step: Get RAG-based answer
        logger.info(f"Processing query: {request.query}")
        rag_result = rag_service.answer_query(request.query)

        # 2️⃣ Step: Get web-based scheme results via LangGraph (optional)
        web_results = []
        if langgraph_service:
            try:
                web_results = langgraph_service.search_scheme(request.query)
            except Exception as e:
                logger.warning(f"LangGraph service failed: {e}")

        # Merge sources (avoid duplicates)
        all_sources = list(dict.fromkeys(rag_result["sources"] + web_results))

        # 3️⃣ Step: Construct final response
        response = QueryResponse(
            eligible=rag_result["eligible"],
            reason=rag_result["reason"],
            confidence=rag_result["confidence"],
            sources=all_sources
        )

        logger.info(f"Query processed successfully. Eligible: {rag_result['eligible']}, Confidence: {rag_result['confidence']}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "rag_service": rag_service is not None,
        "langgraph_service": langgraph_service is not None
    }
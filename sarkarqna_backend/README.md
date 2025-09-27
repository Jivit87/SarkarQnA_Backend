# SarkarQnA Backend

AI-powered government scheme eligibility checker for Indian citizens. Built with FastAPI, LangChain, and HuggingFace models.

## Features

- **Multilingual Support**: Hindi, English, and Hinglish queries
- **RAG Pipeline**: Retrieval-Augmented Generation for accurate answers
- **Free Models**: Uses HuggingFace models (no OpenAI costs)
- **Transliteration**: Automatic Hinglish to Hindi conversion
- **Confidence Scoring**: Reliability metrics for answers
- **Source Attribution**: Shows sources for transparency

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file:

```env
# Optional: HuggingFace API token for better performance
HUGGINGFACE_API_TOKEN=your_hf_token_here

# Optional: LangGraph API key for web search
LANGGRAPH_API_KEY=your_langgraph_key_here

# Optional: OpenAI fallback (if HF token not available)
OPENAI_API_KEY=your_openai_key_here
```

### 3. Prepare Data

1. Add PDF files to `data/schemes_pdf/`
2. Generate embeddings:
   ```python
   # Run this script to create embeddings from PDFs
   python scripts/create_embeddings.py
   ```

### 4. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Check Eligibility
```http
POST /api/check-eligibility
Content-Type: application/json

{
  "query": "मैं किसान हूं, क्या मैं PM-KISAN के लिए योग्य हूं?",
  "language": "hi"
}
```

**Response:**
```json
{
  "eligible": true,
  "reason": "आप PM-KISAN योजना के लिए योग्य हैं क्योंकि...",
  "confidence": 0.85,
  "sources": ["pmkisan.gov.in", "agriculture.gov.in"]
}
```

### Health Check
```http
GET /api/health
```

## Project Structure

```
sarkarqna_backend/
├── main.py                  # FastAPI app entrypoint
├── config.py                # Configuration
├── api/                     # API endpoints
│   └── scheme_router.py
├── schemas/                 # Pydantic models
│   └── request_response.py
├── core/                    # Core business logic
│   ├── models/              # AI models
│   │   └── huggingface_models.py
│   ├── services/            # Business services
│   │   ├── rag_service.py
│   │   ├── langgraph_service.py
│   │   └── preprocessing.py
│   └── utils/               # Utilities
│       └── logger.py
├── data/                    # Data storage
│   ├── schemes_pdf/         # PDF documents
│   ├── embeddings/          # FAISS vectors
│   └── mock_data.json       # Sample data
├── scripts/                 # Utility scripts
│   ├── create_embeddings.py
│   └── test_api.py
└── requirements.txt
```

## Development

### Adding New Schemes

1. Add PDF files to `data/schemes_pdf/`
2. Run embedding generation script
3. Test with sample queries

### Testing

```bash
# Test the API
curl -X POST "http://localhost:8000/api/check-eligibility" \
  -H "Content-Type: application/json" \
  -d '{"query": "I am a farmer, am I eligible for any scheme?"}'
```

## Hackathon Notes

- **Problem**: Citizens struggle with scheme eligibility in local languages
- **Solution**: Multilingual RAG with confidence scoring
- **Tech Stack**: FastAPI + LangChain + HuggingFace + FAISS
- **Metrics**: Top-1/Top-3 accuracy + answer faithfulness
- **Stretch Goals**: Transliteration + confidence scores + source attribution ✅

## License

MIT License - Hackathon Project

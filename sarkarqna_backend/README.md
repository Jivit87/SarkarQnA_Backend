# SarkarQnA Backend

AI-powered government scheme eligibility checker for Indian citizens. Built with FastAPI, LangChain, and HuggingFace models.

## Features

- **Multilingual Support**: Hindi, English, and Hinglish queries
- **RAG Pipeline**: Retrieval-Augmented Generation for accurate answers
- **100% HuggingFace**: Uses only HuggingFace models (completely free)
- **Local Models**: Works offline with local model downloads
- **Transliteration**: Automatic Hinglish to Hindi conversion
- **Confidence Scoring**: Reliability metrics for answers
- **Source Attribution**: Shows sources for transparency
- **No API Costs**: Completely free to run

## Quick Start

### Option A: Automated Setup (Recommended)

```bash
# Run the quick start script (does everything automatically)
python scripts/quick_start.py
```

### Option B: Manual Setup

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Environment Setup

**Option A: Interactive Setup (Recommended)**
```bash
# Run the interactive setup script
python scripts/setup_env.py
```

**Option B: Manual Setup**
```bash
# Copy the template
cp env_template.txt .env

# Edit the .env file with your actual API keys
nano .env  # or use your preferred editor
```

**API Keys (All Optional):**
- **HuggingFace Token** (Optional - For better performance): Get from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- **LangGraph API Key** (Optional - Web search): Get from [langgraph.com](https://langgraph.com/)

**Minimal .env setup for hackathon (works without any API keys):**
```env
# Works completely offline with local models
USE_LOCAL_MODEL=true
DEVICE=cpu
LLM_MODEL=microsoft/DialoGPT-medium
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

**With HuggingFace API token (better performance):**
```env
HUGGINGFACE_API_TOKEN=hf_your_token_here
USE_LOCAL_MODEL=false
LANGGRAPH_API_KEY=your_langgraph_key_here
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
│   ├── setup_env.py
│   ├── quick_start.py
│   └── test_api.py
├── env_template.txt         # Environment template
├── requirements.txt
└── README.md
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

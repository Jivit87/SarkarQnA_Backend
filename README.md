Got it 🚀
Here’s your hackathon-ready README.md in proper Markdown format:

⸻


# 📘 SarkarQnA — AI Scheme Eligibility Bot  

Citizens often struggle to understand whether they are eligible for government schemes, especially in **local languages**. SarkarQnA solves this by using **multilingual AI + RAG (Retrieval-Augmented Generation)** to provide clear, explainable answers.  

---

## 🚀 Features  

- ✅ **Ask in Hindi / Hinglish** → bot understands query  
- ✅ **AI-powered eligibility check** → returns "Eligible / Not Eligible + Why"  
- ✅ **Retrieval-Augmented Generation (RAG)** → answers grounded in official schemes data  
- ✅ **Multilingual embeddings** → Hindi + English support  
- ✅ **Transparent answers** → shows sources + confidence score  
- ✅ **Stretch goals (post-MVP):**  
  - Streaming answers (SSE/WebSocket)  
  - Transliteration Hinglish ↔ Hindi  
  - Push notifications / real-time updates  

---

## 🏗️ Architecture  

```mermaid
graph TD
  A[React Frontend] -->|Query (Hindi/Hinglish)| B[FastAPI Backend]
  B --> C[Preprocessing: Clean + Transliterate]
  C --> D[Embeddings: HF model]
  D --> E[FAISS Vector DB]
  E --> F[RAG Service: RetrievalQA]
  F -->|Answer + Confidence + Sources| A

	•	Frontend: React (chat-like UI, shows eligibility result + sources).
	•	Backend: FastAPI + LangChain + LangGraph (optional for web search).
	•	Models: Hugging Face free models for embeddings + generation.
	•	Data: Curated PDFs/HTML of ~30–50 government schemes, converted to chunks + embeddings.
	•	Storage: FAISS vector store.

⸻

⚙️ Tech Stack
	•	Backend: FastAPI, LangChain, FAISS, LangGraph (optional), Hugging Face
	•	Frontend: React (Vite/CRA/Next.js)
	•	Models (free tier):
	•	Embeddings → sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
	•	LLM → google/flan-t5-small (fallback: gpt-3.5-turbo)

⸻

📂 Folder Structure

sarkarqna/
│── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entrypoint
│   │   ├── routers/
│   │   │   └── scheme_router.py # Eligibility endpoint
│   │   ├── services/
│   │   │   ├── rag_service.py   # RAG pipeline
│   │   │   ├── preprocessing.py # Text cleaning + Hinglish->Hindi
│   │   ├── models/
│   │   │   └── huggingface_models.py
│   │   └── core/
│   │       └── config.py        # Load env vars
│   └── data/
│       ├── schemes_pdf/         # Raw PDFs/HTML of schemes
│       └── embeddings/          # FAISS vector store
│── frontend/
│   ├── src/
│   │   ├── components/ChatUI.js
│   │   └── services/api.js
│── .env.example
│── README.md


⸻

🔑 Environment Setup

Copy .env.example → .env and fill values:

# HuggingFace API Token (Required - free)
HUGGINGFACE_API_TOKEN=hf_your_free_token_here

# OpenAI API Key (Optional - fallback)
OPENAI_API_KEY=sk_your_openai_key_here

# Embedding model
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

# Hugging Face LLM
HF_LLM_MODEL=google/flan-t5-small

# OpenAI fallback model
OPENAI_MODEL=gpt-3.5-turbo

# Paths
EMBEDDING_PATH=data/embeddings
SCHEMES_PDF_PATH=data/schemes_pdf


⸻

🖥️ Backend Setup

cd backend
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Now backend runs at → http://localhost:8000

Example API Request

POST http://localhost:8000/api/check-eligibility
Content-Type: application/json

{
  "query": "Main PM Awas Yojana ke liye eligible hoon kya?",
  "language": "hi"
}

Response:

{
  "eligible": true,
  "reason": "आप PM आवास योजना के लिए योग्य हैं क्योंकि आपकी वार्षिक आय 3 लाख से कम है।",
  "confidence": 0.82,
  "sources": ["pm-awas-yojana.pdf"]
}


⸻

🎨 Frontend Setup

cd frontend
npm install
npm run dev

	•	React app runs on http://localhost:3000
	•	Connects to FastAPI backend via http://localhost:8000/api

⸻

⚡ Streaming (Optional Upgrade)
	•	MVP: Use normal POST → wait for complete answer.
	•	Upgrade: Add SSE or WebSocket for streaming LLM answers.

Example streaming endpoint (/api/stream-eligibility) → client sees answer word-by-word.

⸻

🧪 Evaluation Metrics
	•	Top-1 / Top-3 Retrieval Accuracy (does it fetch correct scheme docs?)
	•	Answer Faithfulness (grounded vs hallucinated)
	•	Latency (time per query)

⸻

🛣️ Roadmap
	•	Hindi/Hinglish preprocessing
	•	RAG pipeline with FAISS + HF embeddings
	•	Eligibility classifier (keyword-based)
	•	Streaming answers via SSE
	•	Web search via LangGraph (live scheme updates)
	•	Confidence calibration (cosine similarity scores)
	•	User feedback loop (thumbs up/down)

⸻

👨‍💻 Team & Learning
	•	Hackathon Goal: Hands-on with LangChain + LangGraph + RAG + Hugging Face
	•	Learning Outcomes:
	•	Build multilingual RAG pipelines
	•	Handle retrieval + re-ranking for real-world data
	•	Deploy FastAPI + React full stack AI app

⸻

📜 License

MIT License — free to use, modify, and share.

---

Would you like me to also create a **lightweight README for the judges (1-page version)** with **screenshots/mockups + demo steps only**, so you can attach it separately as a quick guide?

# 🔑 API Setup Instructions

## Google Gemini API Key Setup

To enable real AI responses instead of demo mode, you need to configure the Google Gemini API key:

### Step 1: Get Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### Step 2: Configure Backend
1. Open the `.env` file in the backend directory:
   ```
   /SarkarQnA_Backend/sarkarqna_backend/.env
   ```

2. Replace `your_gemini_api_key_here` with your actual API key:
   ```env
   GEMINI_API_KEY=AIzaSyC-your-actual-api-key-here
   ```

3. Save the file

### Step 3: Restart Backend
The backend should automatically reload. If not, restart it:
```bash
cd /path/to/SarkarQnA_Backend/sarkarqna_backend
source venv/bin/activate
python -m uvicorn main:app --reload --port 8000
```

## Current Status
- ✅ Backend running in **demo mode** (no API key required)
- ✅ Socket connections working properly
- ✅ Demo responses provided for all queries
- 🔧 **Add API key for real AI responses**

## Demo Mode Features
Without API key, the backend provides:
- Intelligent keyword-based responses
- Government scheme information
- Eligibility guidance
- Professional formatting

## With API Key
After adding the Gemini API key:
- Real AI-powered responses
- Advanced natural language understanding
- Dynamic scheme analysis
- Personalized recommendations

---
*Note: The API key is free with generous quotas for development and testing.*

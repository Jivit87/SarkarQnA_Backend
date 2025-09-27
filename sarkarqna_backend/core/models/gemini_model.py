import google.generativeai as genai
from typing import Optional
from core.utils.logger import logger
from config import settings

class GeminiModel:
    def __init__(self):
        """Initialize Gemini model with API key from settings"""
        self.model = None
        self.demo_mode = False
        
        try:
            if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini model initialized successfully with API key")
            else:
                logger.warning("Gemini API key not configured. Running in demo mode.")
                self.demo_mode = True
                logger.info("Gemini model initialized in demo mode")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}. Falling back to demo mode.")
            self.demo_mode = True
            self.model = None

    async def generate_response(self, message: str) -> dict:
        """Generate response using Gemini model or demo mode"""
        try:
            if self.demo_mode or not self.model:
                # Demo mode - provide intelligent mock responses
                return self._generate_demo_response(message)
            
            # Check if the message is about scheme eligibility
            is_eligibility_query = self._check_if_eligibility_query(message)
            
            # Generate response using real Gemini API
            response = self.model.generate_content(message)
            
            return {
                "text": response.text,
                "is_eligibility_query": is_eligibility_query
            }
        except Exception as e:
            logger.error(f"Error generating Gemini response: {e}. Using demo response.")
            return self._generate_demo_response(message)

    def _generate_demo_response(self, message: str) -> dict:
        """Generate demo response when API key is not available"""
        message_lower = message.lower()
        
        # Check if it's an eligibility query
        eligibility_keywords = ['eligible', 'qualify', 'पात्र', 'योग्य', 'scheme', 'योजना', 'benefit', 'apply']
        is_eligibility_query = any(keyword in message_lower for keyword in eligibility_keywords)
        
        if is_eligibility_query:
            demo_text = """🎯 **Demo Mode Response** 

Based on your query, I can provide general guidance about government schemes:

**Common Government Schemes:**
• **PM-KISAN**: For farmers with agricultural land
• **Ayushman Bharat**: Health insurance for eligible families  
• **PM Awas Yojana**: Housing assistance for economically weaker sections
• **MGNREGA**: Employment guarantee for rural households

**To check eligibility:**
1. Visit the official scheme website
2. Verify your documents (Aadhaar, income certificate, etc.)
3. Apply through proper channels

*Note: This is a demo response. For real eligibility checking, please configure the Gemini API key in the backend .env file.*"""
        else:
            demo_text = """🤖 **Demo Mode Response**

Hello! I'm SarkarQnA, your AI assistant for government schemes and services.

I can help you with:
• Government scheme eligibility
• Application processes  
• Required documents
• Benefits and features

*Note: This is a demo response. For real AI responses, please configure the Gemini API key in the backend .env file.*

How can I assist you today?"""

        return {
            "text": demo_text,
            "is_eligibility_query": is_eligibility_query
        }

    def _check_if_eligibility_query(self, message: str) -> bool:
        """Check if the message is asking about scheme eligibility"""
        try:
            if self.demo_mode or not self.model:
                # Simple keyword-based check for demo mode
                eligibility_keywords = ['eligible', 'qualify', 'पात्र', 'योग्य', 'scheme', 'योजना', 'benefit', 'apply']
                return any(keyword in message.lower() for keyword in eligibility_keywords)
                
            # Use real Gemini API
            check_prompt = f"""Analyze if this message is asking about eligibility for any government scheme or program. 
            Return only 'true' or 'false'.
            Message: {message}"""
            
            response = self.model.generate_content(check_prompt)
            return response.text.strip().lower() == 'true'
            
        except Exception as e:
            logger.error(f"Error checking eligibility query: {e}")
            return False
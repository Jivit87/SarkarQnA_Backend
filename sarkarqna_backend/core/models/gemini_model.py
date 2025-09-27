import google.generativeai as genai
from typing import Optional
from core.utils.logger import logger
from config import settings

class GeminiModel:
    def __init__(self):
        """Initialize Gemini model with API key from settings"""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Gemini model initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")
            raise

    async def generate_response(self, message: str) -> dict:
        """Generate response using Gemini model"""
        try:
            # Check if the message is about scheme eligibility
            is_eligibility_query = self._check_if_eligibility_query(message)
            
            # Generate response
            response = self.model.generate_content(message)
            
            return {
                "text": response.text,
                "is_eligibility_query": is_eligibility_query
            }
        except Exception as e:
            logger.error(f"Error generating Gemini response: {e}")
            raise

    def _check_if_eligibility_query(self, message: str) -> bool:
        """Check if the message is asking about scheme eligibility"""
        try:
            # Create a prompt to check if this is an eligibility query
            check_prompt = f"""Analyze if this message is asking about eligibility for any government scheme or program. 
            Return only 'true' or 'false'.
            Message: {message}"""
            
            response = self.model.generate_content(check_prompt)
            return response.text.strip().lower() == 'true'
            
        except Exception as e:
            logger.error(f"Error checking eligibility query: {e}")
            return False
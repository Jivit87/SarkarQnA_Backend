# core/services/preprocessing.py

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import re

class Preprocessing:
    def __init__(self):
        pass

    def clean_text(self, text: str) -> str:
        """Remove extra spaces, special characters, normalize text."""
        text = re.sub(r'\s+', ' ', text)  # normalize whitespace
        text = re.sub(r'[^\w\s]', '', text)  # remove punctuation
        return text.strip()

    def hinglish_to_hindi(self, text: str) -> str:
        """
        Transliterate Hinglish (Latin script) to Hindi (Devanagari).
        Works best for simple Hindi words typed in Latin script.
        """
        try:
            return transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
        except Exception:
            return text  # fallback if transliteration fails


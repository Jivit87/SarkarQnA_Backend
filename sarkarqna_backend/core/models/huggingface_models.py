# app/models/huggingface_models.py

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain_community.chat_models import ChatOpenAI
import os

class HFModels:
    def __init__(self):
        # Multilingual embedding model (supports Hindi, English, Hinglish)
        self.embedding_model_name = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model_name,
            model_kwargs={'device': 'cpu'}  # Use CPU for free tier
        )

        # Use HuggingFace free model instead of OpenAI
        hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
        if hf_token:
            self.llm = HuggingFaceHub(
                repo_id="microsoft/DialoGPT-medium",  # Free multilingual model
                huggingfacehub_api_token=hf_token,
                model_kwargs={"temperature": 0.1, "max_length": 512}
            )
        else:
            # Fallback to OpenAI if HF token not available
            self.llm = ChatOpenAI(
                model_name=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                temperature=0
            )

    def get_embeddings(self):
        return self.embeddings

    def get_llm(self):
        return self.llm
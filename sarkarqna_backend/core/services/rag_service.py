# app/services/rag_service.py

from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from core.models.huggingface_models import HFModels
from core.services.preprocessing import Preprocessing
from typing import List
import os

class RAGService:
    def __init__(self, embedding_path: str = "data/embeddings"):
        # Initialize models and preprocessing
        self.hf_models = HFModels()
        self.preprocess = Preprocessing()
        self.embedding_path = embedding_path

        # Load embeddings from FAISS (with error handling)
        self.embeddings = self.hf_models.get_embeddings()
        try:
            self.vectorstore = FAISS.load_local(embedding_path, self.embeddings, allow_dangerous_deserialization=True)
            self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
            
            # QA Chain for answer generation
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.hf_models.get_llm(),
                retriever=self.retriever,
                chain_type="stuff"
            )
        except Exception as e:
            print(f"Warning: Could not load FAISS embeddings from {embedding_path}: {e}")
            self.vectorstore = None
            self.retriever = None
            self.qa_chain = None

    def answer_query(self, query: str) -> dict:
        """
        Process user query and return:
        - eligibility answer
        - confidence score (based on FAISS similarity)
        - sources
        """
        # Handle case where embeddings are not loaded
        if not self.retriever or not self.qa_chain:
            return {
                "eligible": False,
                "reason": "Service not available - embeddings not loaded. Please check if data/embeddings directory exists.",
                "confidence": 0.0,
                "sources": []
            }

        # Step 1: Clean + transliterate query
        clean_query = self.preprocess.clean_text(query)
        query_in_hindi = self.preprocess.hinglish_to_hindi(clean_query)

        try:
            # Step 2: Retrieve relevant documents
            docs = self.retriever.get_relevant_documents(query_in_hindi)
            top_sources = [doc.metadata.get("source", "Unknown") for doc in docs]

            # Step 3: Generate answer
            rag_answer = self.qa_chain.run(query_in_hindi)

            # Step 4: Compute confidence (average similarity from docs)
            if docs and hasattr(docs[0], 'score'):
                avg_confidence = sum([doc.score for doc in docs]) / len(docs)
            else:
                # Fallback confidence based on document count
                avg_confidence = min(len(docs) / 3.0, 1.0)

            # Step 5: Determine eligibility (enhanced keyword matching)
            eligible_keywords = ["eligible", "योग्य", "हैं", "qualify", "entitled"]
            not_eligible_keywords = ["not eligible", "अयोग्य", "not qualify", "not entitled"]
            
            rag_lower = rag_answer.lower()
            is_eligible = any(word.lower() in rag_lower for word in eligible_keywords)
            is_not_eligible = any(word.lower() in rag_lower for word in not_eligible_keywords)
            
            # If both found, prioritize not eligible
            if is_not_eligible:
                is_eligible = False

            return {
                "eligible": is_eligible,
                "reason": rag_answer,
                "confidence": round(avg_confidence, 2),
                "sources": top_sources
            }
            
        except Exception as e:
            return {
                "eligible": False,
                "reason": f"Error processing query: {str(e)}",
                "confidence": 0.0,
                "sources": []
            }
#!/usr/bin/env python3
"""
Script to create embeddings from PDF documents for RAG pipeline
"""

import os
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.models.huggingface_models import HFModels
from core.utils.logger import logger

def create_embeddings_from_pdfs():
    """Create embeddings from PDF files in data/schemes_pdf/"""
    
    # Paths
    pdf_dir = Path("data/schemes_pdf")
    embedding_dir = Path("data/embeddings")
    mock_data_path = Path("data/mock_data.json")
    
    # Create directories if they don't exist
    embedding_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize models
    logger.info("Initializing HuggingFace models...")
    hf_models = HFModels()
    embeddings = hf_models.get_embeddings()
    
    all_documents = []
    
    # Load from PDFs if they exist
    if pdf_dir.exists() and any(pdf_dir.glob("*.pdf")):
        logger.info(f"Loading PDFs from {pdf_dir}")
        for pdf_file in pdf_dir.glob("*.pdf"):
            try:
                loader = PyPDFLoader(str(pdf_file))
                documents = loader.load()
                for doc in documents:
                    doc.metadata["source"] = pdf_file.name
                all_documents.extend(documents)
                logger.info(f"Loaded {len(documents)} pages from {pdf_file.name}")
            except Exception as e:
                logger.error(f"Error loading {pdf_file}: {e}")
    
    # Load from mock data if no PDFs or as fallback
    if not all_documents and mock_data_path.exists():
        logger.info("Loading from mock data...")
        with open(mock_data_path, 'r', encoding='utf-8') as f:
            mock_data = json.load(f)
        
        for scheme in mock_data.get("schemes", []):
            # Create document from scheme data
            content = f"""
            Scheme: {scheme['name']}
            Description: {scheme['description']}
            Eligibility Criteria: {', '.join(scheme['eligibility_criteria'])}
            Benefits: {scheme['benefits']}
            """
            
            from langchain.schema import Document
            doc = Document(
                page_content=content,
                metadata={
                    "source": scheme.get("source", "mock_data"),
                    "scheme_name": scheme['name'],
                    "language": scheme.get("language", "hindi")
                }
            )
            all_documents.append(doc)
    
    if not all_documents:
        logger.error("No documents found to create embeddings from!")
        return False
    
    # Split documents into chunks
    logger.info("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    split_documents = text_splitter.split_documents(all_documents)
    logger.info(f"Created {len(split_documents)} document chunks")
    
    # Create FAISS vectorstore
    logger.info("Creating FAISS vectorstore...")
    vectorstore = FAISS.from_documents(split_documents, embeddings)
    
    # Save vectorstore
    logger.info(f"Saving embeddings to {embedding_dir}")
    vectorstore.save_local(str(embedding_dir))
    
    logger.info("Embeddings created successfully!")
    return True

if __name__ == "__main__":
    success = create_embeddings_from_pdfs()
    if success:
        print("✅ Embeddings created successfully!")
    else:
        print("❌ Failed to create embeddings")
        sys.exit(1)

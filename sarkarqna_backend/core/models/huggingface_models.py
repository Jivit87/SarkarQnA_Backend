# core/models/huggingface_models.py

from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.llms import HuggingFaceHub
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from config import settings

class HFModels:
    def __init__(self):
        # Multilingual embedding model (supports Hindi, English, Hinglish)
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={'device': settings.DEVICE},
            encode_kwargs={'normalize_embeddings': True}
        )

        # HuggingFace LLM setup
        self.llm = self._setup_llm()
    
    def _setup_llm(self):
        """Setup the LLM based on configuration"""
        
        if settings.HUGGINGFACE_API_TOKEN and not settings.USE_LOCAL_MODEL:
            # Use HuggingFace Hub with API token
            return HuggingFaceHub(
                repo_id=settings.LLM_MODEL,
                huggingfacehub_api_token=settings.HUGGINGFACE_API_TOKEN,
                model_kwargs={
                    "temperature": settings.TEMPERATURE,
                    "max_length": settings.MAX_LENGTH,
                    "do_sample": settings.DO_SAMPLE,
                    "pad_token_id": 50256
                }
            )
        else:
            # Use local model (no API token needed)
            try:
                print(f"Loading local model: {settings.LLM_MODEL}")
                
                # Load model locally for better performance
                tokenizer = AutoTokenizer.from_pretrained(settings.LLM_MODEL)
                
                # Add padding token if not present
                if tokenizer.pad_token is None:
                    tokenizer.pad_token = tokenizer.eos_token
                
                model = AutoModelForCausalLM.from_pretrained(
                    settings.LLM_MODEL,
                    dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    device_map="auto" if torch.cuda.is_available() else None,
                    low_cpu_mem_usage=True
                )
                
                # Create pipeline
                pipe = pipeline(
                    "text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    max_length=settings.MAX_LENGTH,
                    temperature=settings.TEMPERATURE,
                    do_sample=settings.DO_SAMPLE,
                    pad_token_id=tokenizer.pad_token_id,
                    device=0 if torch.cuda.is_available() else -1
                )
                
                return HuggingFacePipeline(pipeline=pipe)
                
            except Exception as e:
                print(f"Warning: Could not load local model {settings.LLM_MODEL}: {e}")
                print("Falling back to GPT-2...")
                
                # Fallback to a smaller model
                try:
                    tokenizer = AutoTokenizer.from_pretrained("gpt2")
                    model = AutoModelForCausalLM.from_pretrained("gpt2")
                    
                    pipe = pipeline(
                        "text-generation",
                        model=model,
                        tokenizer=tokenizer,
                        max_length=256,
                        temperature=0.1,
                        do_sample=True,
                        pad_token_id=tokenizer.eos_token_id
                    )
                    
                    return HuggingFacePipeline(pipeline=pipe)
                    
                except Exception as e2:
                    print(f"Error loading fallback model: {e2}")
                    # Last resort - use HuggingFace Hub without token
                    return HuggingFaceHub(
                        repo_id="gpt2",
                        model_kwargs={"temperature": 0.1, "max_length": 256}
                    )

    def get_embeddings(self):
        return self.embeddings

    def get_llm(self):
        return self.llm
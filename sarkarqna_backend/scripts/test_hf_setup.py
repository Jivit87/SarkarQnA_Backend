#!/usr/bin/env python3
"""
Test script for HuggingFace setup
This script tests if the HuggingFace models are working correctly
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

def test_imports():
    """Test if all required imports work"""
    print("🔍 Testing imports...")
    
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
        print(f"   CUDA available: {torch.cuda.is_available()}")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        import transformers
        print(f"✅ Transformers: {transformers.__version__}")
    except ImportError as e:
        print(f"❌ Transformers import failed: {e}")
        return False
    
    try:
        import sentence_transformers
        print(f"✅ Sentence Transformers: {sentence_transformers.__version__}")
    except ImportError as e:
        print(f"❌ Sentence Transformers import failed: {e}")
        return False
    
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.llms import HuggingFaceHub
        print("✅ LangChain HuggingFace components")
    except ImportError as e:
        print(f"❌ LangChain HuggingFace import failed: {e}")
        return False
    
    return True

def test_models():
    """Test if models can be loaded"""
    print("\n🤖 Testing model loading...")
    
    try:
        from core.models.huggingface_models import HFModels
        print("✅ HFModels class imported successfully")
        
        # Test embeddings
        print("   Testing embeddings...")
        hf_models = HFModels()
        embeddings = hf_models.get_embeddings()
        print("✅ Embeddings loaded successfully")
        
        # Test LLM
        print("   Testing LLM...")
        llm = hf_models.get_llm()
        print("✅ LLM loaded successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import settings
        print("✅ Configuration loaded successfully")
        print(f"   Embedding Model: {settings.EMBEDDING_MODEL}")
        print(f"   LLM Model: {settings.LLM_MODEL}")
        print(f"   Device: {settings.DEVICE}")
        print(f"   Use Local Model: {settings.USE_LOCAL_MODEL}")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_simple_inference():
    """Test simple inference"""
    print("\n🧪 Testing simple inference...")
    
    try:
        from core.models.huggingface_models import HFModels
        
        hf_models = HFModels()
        llm = hf_models.get_llm()
        
        # Simple test
        test_prompt = "Hello, how are you?"
        print(f"   Testing with prompt: '{test_prompt}'")
        
        # This might take a moment on first run
        response = llm(test_prompt)
        print(f"✅ Inference successful!")
        print(f"   Response: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Inference test failed: {e}")
        return False

def main():
    """Main test function"""
    
    print("🚀 HuggingFace Setup Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_config),
        ("Model Loading Test", test_models),
        ("Inference Test", test_simple_inference)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! HuggingFace setup is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

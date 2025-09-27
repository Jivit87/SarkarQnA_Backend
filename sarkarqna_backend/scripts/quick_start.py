#!/usr/bin/env python3
"""
Quick Start Script for SarkarQnA Backend
This script sets up everything needed to run the SarkarQnA backend
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible!")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    return run_command("pip install -r requirements.txt", "Installing dependencies")

def setup_environment():
    """Setup environment configuration"""
    print("\n🔧 Setting up environment...")
    
    # Check if .env exists
    env_path = Path(".env")
    if env_path.exists():
        print("✅ .env file already exists!")
        return True
    
    # Run the setup script
    setup_script = Path("scripts/setup_env.py")
    if setup_script.exists():
        return run_command(f"python {setup_script}", "Environment setup")
    else:
        print("⚠️  Setup script not found. Please create .env file manually.")
        return False

def create_embeddings():
    """Create embeddings from data"""
    print("\n🧮 Creating embeddings...")
    
    # Check if embeddings already exist
    embeddings_path = Path("data/embeddings")
    if embeddings_path.exists() and any(embeddings_path.iterdir()):
        print("✅ Embeddings already exist!")
        return True
    
    # Run embedding creation script
    embedding_script = Path("scripts/create_embeddings.py")
    if embedding_script.exists():
        return run_command(f"python {embedding_script}", "Creating embeddings")
    else:
        print("⚠️  Embedding script not found. Please create embeddings manually.")
        return False

def test_server():
    """Test if the server can start"""
    print("\n🧪 Testing server startup...")
    
    # Try to import the main module
    try:
        import main
        print("✅ Server module imports successfully!")
        return True
    except ImportError as e:
        print(f"❌ Server import failed: {e}")
        return False

def main():
    """Main quick start function"""
    
    print("🚀 SarkarQnA Backend Quick Start")
    print("=" * 50)
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies!")
        print("Please check your Python environment and try again.")
        sys.exit(1)
    
    # Step 3: Setup environment
    if not setup_environment():
        print("\n⚠️  Environment setup incomplete!")
        print("Please configure your API keys in the .env file.")
    
    # Step 4: Create embeddings
    if not create_embeddings():
        print("\n⚠️  Embeddings creation failed!")
        print("Please check your data and try again.")
    
    # Step 5: Test server
    if not test_server():
        print("\n❌ Server test failed!")
        print("Please check your configuration and try again.")
        sys.exit(1)
    
    # Success!
    print("\n🎉 SarkarQnA Backend is ready!")
    print("\n📖 Next steps:")
    print("   1. Start the server: uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("   2. Test the API: python scripts/test_api.py")
    print("   3. Open browser: http://localhost:8000/docs")
    
    print("\n🔗 Useful URLs:")
    print("   • API Documentation: http://localhost:8000/docs")
    print("   • Health Check: http://localhost:8000/health")
    print("   • Root Endpoint: http://localhost:8000/")

if __name__ == "__main__":
    main()

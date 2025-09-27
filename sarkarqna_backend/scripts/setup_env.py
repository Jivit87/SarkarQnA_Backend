#!/usr/bin/env python3
"""
Setup script for SarkarQnA Backend Environment
This script helps you configure your .env file with API keys
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file from template"""
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    template_path = project_root / "env_template.txt"
    env_path = project_root / ".env"
    
    if env_path.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ").lower()
        if response != 'y':
            print("❌ Setup cancelled.")
            return False
    
    if not template_path.exists():
        print(f"❌ Template file not found: {template_path}")
        return False
    
    # Copy template to .env
    with open(template_path, 'r') as template:
        content = template.read()
    
    with open(env_path, 'w') as env_file:
        env_file.write(content)
    
    print(f"✅ Created .env file at {env_path}")
    return True

def interactive_setup():
    """Interactive setup for API keys"""
    
    print("\n🔧 Interactive API Key Setup")
    print("=" * 50)
    
    # HuggingFace Token
    print("\n1. HuggingFace API Token (Optional - For better performance)")
    print("   Get your token from: https://huggingface.co/settings/tokens")
    print("   Note: You can skip this and use local models instead!")
    hf_token = input("   Enter your HuggingFace token (or press Enter to skip): ").strip()
    
    # LangGraph API Key
    print("\n2. LangGraph API Key (Optional - Web search)")
    print("   Get your key from: https://langgraph.com/")
    langgraph_key = input("   Enter your LangGraph API key (or press Enter to skip): ").strip()
    
    # Model Configuration
    print("\n3. Model Configuration")
    use_local = input("   Use local models? (Y/n): ").lower()
    use_local = use_local != 'n'
    
    device = input("   Device (cpu/cuda/auto) [cpu]: ").strip() or "cpu"
    
    # Update .env file with actual keys
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Replace placeholder values
        if hf_token:
            content = content.replace("your_huggingface_token_here", hf_token)
        if langgraph_key:
            content = content.replace("your_langgraph_key_here", langgraph_key)
        
        # Update model configuration
        content = content.replace("USE_LOCAL_MODEL=true", f"USE_LOCAL_MODEL={str(use_local).lower()}")
        content = content.replace("DEVICE=cpu", f"DEVICE={device}")
        
        with open(env_path, 'w') as f:
            f.write(content)
        
        print("\n✅ Environment configured successfully!")
        print(f"📁 .env file updated at: {env_path}")
        
        # Show summary
        print("\n📋 Configuration Summary:")
        print(f"   HuggingFace Token: {'✅ Set' if hf_token else '❌ Not set (will use local models)'}")
        print(f"   LangGraph API Key: {'✅ Set' if langgraph_key else '❌ Not set'}")
        print(f"   Use Local Models: {'✅ Yes' if use_local else '❌ No (using API)'}")
        print(f"   Device: {device}")
        
        return True
    else:
        print("❌ .env file not found. Please run create_env_file() first.")
        return False

def main():
    """Main setup function"""
    
    print("🚀 SarkarQnA Backend Environment Setup")
    print("=" * 50)
    
    # Step 1: Create .env file
    print("\n📝 Step 1: Creating .env file...")
    if not create_env_file():
        sys.exit(1)
    
    # Step 2: Interactive setup
    print("\n🔧 Step 2: Configure API keys...")
    response = input("Do you want to configure API keys now? (Y/n): ").lower()
    
    if response != 'n':
        if interactive_setup():
            print("\n🎉 Setup completed successfully!")
            print("\n📖 Next steps:")
            print("   1. Install dependencies: pip install -r requirements.txt")
            print("   2. Create embeddings: python scripts/create_embeddings.py")
            print("   3. Run the server: uvicorn main:app --reload")
        else:
            print("\n⚠️  Setup incomplete. You can manually edit the .env file later.")
    else:
        print("\n📝 You can manually edit the .env file later with your API keys.")
    
    print("\n✅ Environment setup complete!")

if __name__ == "__main__":
    main()

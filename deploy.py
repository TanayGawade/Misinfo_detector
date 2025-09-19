#!/usr/bin/env python3
"""
Streamlit Deployment Helper for Misinformation Detection System
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if required files exist"""
    required_files = [
        "streamlitui.py",
        "requirements.txt", 
        ".env.example",
        "app/agent.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    return True

def check_env_vars():
    """Check if environment variables are set"""
    if not Path(".env").exists():
        print("⚠️  .env file not found. Please create it from .env.example")
        print("   Make sure to add your GEMINI_API_KEY")
        return False
    
    # Read .env file and check for GEMINI_API_KEY
    with open(".env", "r") as f:
        env_content = f.read()
        if "GEMINI_API_KEY=" not in env_content or "your-gemini-api-key-here" in env_content:
            print("⚠️  GEMINI_API_KEY not properly set in .env file")
            return False
    
    print("✅ Environment variables configured")
    return True

def test_streamlit_app():
    """Test the Streamlit application"""
    print("\n🧪 Testing Streamlit app...")
    
    try:
        sys.path.append(".")
        import streamlitui
        from app import agent
        print("✅ Streamlit app imports successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def show_deployment_guide():
    """Show Streamlit deployment guide"""
    print("\n🚀 Streamlit Cloud Deployment (FREE):")
    print("\n1. 📤 Push to GitHub:")
    print("   git add .")
    print("   git commit -m 'Deploy to Streamlit Cloud'")
    print("   git push origin main")
    
    print("\n2. 🌐 Deploy on Streamlit Cloud:")
    print("   • Go to: https://share.streamlit.io")
    print("   • Sign in with GitHub")
    print("   • Click 'New app'")
    print("   • Select your repository")
    print("   • Set main file: streamlitui.py")
    print("   • Add GEMINI_API_KEY in secrets")
    print("   • Click 'Deploy'")
    
    print("\n3. 🎉 Your app will be live at:")
    print("   https://your-app-name.streamlit.app")

def main():
    """Main deployment preparation function"""
    print("🎨 Streamlit Deployment Helper")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment variables
    if not check_env_vars():
        print("\n📝 To fix this:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env and add your GEMINI_API_KEY")
        print("3. Get API key from: https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    # Test Streamlit app
    if not test_streamlit_app():
        sys.exit(1)
    
    print("\n✅ All checks passed! Your Streamlit app is ready for deployment.")
    
    # Show deployment guide
    show_deployment_guide()
    
    print("\n📋 For detailed instructions, see DEPLOYMENT.md")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Test script to verify Streamlit app functionality
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        # Test Streamlit
        import streamlit as st
        print("✅ Streamlit imported successfully")
        
        # Test Google Generative AI
        import google.generativeai as genai
        print("✅ Google Generative AI imported successfully")
        
        # Test dotenv
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
        
        # Test our modules
        sys.path.append(".")
        from app.agent import run_analysis
        print("✅ AI agent imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_env_setup():
    """Test environment setup"""
    print("\n🔧 Testing environment setup...")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  GEMINI_API_KEY not found in environment")
        return False
    elif "your-gemini-api-key-here" in api_key:
        print("⚠️  GEMINI_API_KEY still has placeholder value")
        return False
    else:
        print("✅ GEMINI_API_KEY configured")
        return True

def test_streamlit_syntax():
    """Test if streamlitui.py has valid syntax"""
    print("\n📝 Testing Streamlit app syntax...")
    
    try:
        with open("streamlitui.py", "r", encoding="utf-8") as f:
            code = f.read()
        
        # Compile to check syntax
        compile(code, "streamlitui.py", "exec")
        print("✅ Streamlit app syntax is valid")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error in streamlitui.py: {e}")
        return False
    except FileNotFoundError:
        print("❌ streamlitui.py not found")
        return False
    except UnicodeDecodeError as e:
        print(f"❌ Encoding error in streamlitui.py: {e}")
        print("   Try saving the file with UTF-8 encoding")
        return False

def main():
    """Run all tests"""
    print("🎨 Streamlit App Test Suite")
    print("=" * 30)
    
    tests = [
        test_imports,
        test_env_setup,
        test_streamlit_syntax
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Streamlit app is ready to deploy.")
        print("\n🚀 To deploy:")
        print("1. Run: python deploy.py")
        print("2. Follow the Streamlit Cloud deployment guide")
    else:
        print("❌ Some tests failed. Please fix the issues before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main()
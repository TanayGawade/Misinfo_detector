#!/usr/bin/env python3
"""
Test script for the Gemini-powered AI agent.

This script tests the updated AI agent functionality with Google Gemini integration.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

async def test_gemini_agent():
    """Test the Gemini-powered AI agent."""
    print("🤖 Testing Gemini AI Agent Integration")
    print("="*50)
    
    try:
        from app.agent import run_analysis
        
        # Test cases with different types of content
        test_cases = [
            {
                "name": "Scientific Fact",
                "content": "Water boils at 100 degrees Celsius at sea level atmospheric pressure."
            },
            {
                "name": "Controversial Claim",
                "content": "Vaccines cause autism and should be avoided by all children."
            },
            {
                "name": "Climate Science",
                "content": "Climate change is primarily caused by human activities, particularly the burning of fossil fuels."
            },
            {
                "name": "Conspiracy Theory",
                "content": "The moon landing in 1969 was filmed in a Hollywood studio and never actually happened."
            },
            {
                "name": "Health Misinformation",
                "content": "Drinking bleach can cure COVID-19 and other viral infections."
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}: {test_case['name']}")
            print(f"Content: {test_case['content']}")
            print("-" * 50)
            
            try:
                # Run analysis
                result = await run_analysis(test_case['content'])
                
                # Display results
                print(f"✅ Verdict: {result['verdict']}")
                print(f"📊 Credibility Score: {result['credibility_score']:.2f}")
                print(f"📝 Explanation: {result['explanation']}")
                print(f"🔍 Claims Analyzed: {result['claims_analyzed']}")
                print(f"📚 Sources Consulted: {result['sources_consulted']}")
                
                if result['sources']:
                    print("📖 Sources:")
                    for j, source in enumerate(result['sources'][:3], 1):  # Show first 3 sources
                        print(f"  {j}. {source.get('title', 'Unknown')} (Credibility: {source.get('credibility', 'unknown')})")
                
                results.append({
                    "test_case": test_case['name'],
                    "verdict": result['verdict'],
                    "score": result['credibility_score'],
                    "success": True
                })
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                results.append({
                    "test_case": test_case['name'],
                    "verdict": "ERROR",
                    "score": 0.0,
                    "success": False,
                    "error": str(e)
                })
        
        # Summary
        print("\n" + "="*50)
        print("📊 TEST SUMMARY")
        print("="*50)
        
        successful_tests = sum(1 for r in results if r['success'])
        total_tests = len(results)
        
        print(f"✅ Successful Tests: {successful_tests}/{total_tests}")
        print(f"📈 Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        
        print("\n📋 Results Overview:")
        for result in results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test_case']}: {result['verdict']} (Score: {result['score']:.2f})")
        
        # Check if Gemini is actually being used
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if gemini_api_key:
            print(f"\n🔑 Gemini API Key: Configured (length: {len(gemini_api_key)})")
            print("🚀 Using Google Gemini for AI analysis")
        else:
            print("\n⚠️  Gemini API Key: Not configured")
            print("🔄 Using fallback analysis methods")
        
        return successful_tests == total_tests
        
    except Exception as e:
        print(f"❌ Test setup failed: {str(e)}")
        return False

async def test_gemini_configuration():
    """Test Gemini configuration and connectivity."""
    print("\n🔧 Testing Gemini Configuration")
    print("="*50)
    
    try:
        import google.generativeai as genai
        
        # Check API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️  GEMINI_API_KEY not set in environment")
            print("💡 To use Gemini, set your API key:")
            print("   export GEMINI_API_KEY='your-api-key-here'")
            print("   or add it to your .env file")
            return False
        
        print(f"✅ API Key configured (length: {len(api_key)})")
        
        # Test model configuration
        model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        print(f"✅ Model: {model_name}")
        
        # Test basic connectivity (if API key is provided)
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(model_name)
            
            # Simple test prompt
            response = await asyncio.to_thread(
                model.generate_content, 
                "Respond with just the word 'SUCCESS' if you can read this."
            )
            
            if "SUCCESS" in response.text.upper():
                print("✅ Gemini connectivity test passed")
                return True
            else:
                print(f"⚠️  Unexpected response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Gemini connectivity test failed: {str(e)}")
            print("💡 Please check your API key and internet connection")
            return False
        
    except ImportError as e:
        print(f"❌ Gemini library not available: {str(e)}")
        print("💡 Install with: pip install google-generativeai")
        return False

def main():
    """Main test function."""
    print("🧪 GEMINI AI AGENT TEST SUITE")
    print("="*60)
    
    # Test configuration first
    config_success = asyncio.run(test_gemini_configuration())
    
    # Test agent functionality
    agent_success = asyncio.run(test_gemini_agent())
    
    print("\n" + "="*60)
    print("🎯 FINAL RESULTS")
    print("="*60)
    
    if config_success and agent_success:
        print("🎉 All tests passed! Gemini integration is working correctly.")
        print("🚀 The misinformation detection system is now powered by Google Gemini!")
        return True
    elif agent_success:
        print("✅ Agent tests passed with fallback methods.")
        print("💡 Configure GEMINI_API_KEY to enable full Gemini integration.")
        return True
    else:
        print("❌ Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
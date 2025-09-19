#!/usr/bin/env python3
"""
Quick test script to verify agent.py functionality
"""

import asyncio
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from agent import run_analysis

async def test_agent():
    """Test the agent analysis function"""
    test_content = "The Earth is flat and NASA is hiding the truth. Scientists have proven this fact."
    
    try:
        result = await run_analysis(test_content)
        print("✅ Agent analysis completed successfully!")
        print(f"Verdict: {result['verdict']}")
        print(f"Explanation: {result['explanation']}")
        print(f"Sources found: {len(result['sources'])}")
        print(f"Credibility score: {result['credibility_score']:.2f}")
        return True
    except Exception as e:
        print(f"❌ Agent analysis failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agent())
    sys.exit(0 if success else 1)
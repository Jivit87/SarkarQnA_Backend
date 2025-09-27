#!/usr/bin/env python3
"""
Simple test script for SarkarQnA API
"""

import requests
import json

def test_api():
    """Test the SarkarQnA API endpoints"""
    
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test eligibility endpoint
    print("\n🔍 Testing eligibility endpoint...")
    
    test_queries = [
        {
            "query": "मैं किसान हूं, क्या मैं PM-KISAN के लिए योग्य हूं?",
            "language": "hi"
        },
        {
            "query": "I am a farmer with 2 acres land, am I eligible for any scheme?",
            "language": "en"
        },
        {
            "query": "मेरी आय 5 लाख है, क्या मैं PMAY के लिए योग्य हूं?",
            "language": "hi"
        }
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test Query {i} ---")
        print(f"Query: {query['query']}")
        
        try:
            response = requests.post(
                f"{base_url}/api/check-eligibility",
                json=query,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Eligible: {result['eligible']}")
                print(f"📊 Confidence: {result['confidence']}")
                print(f"💭 Reason: {result['reason'][:100]}...")
                print(f"📚 Sources: {result['sources']}")
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("🚀 Testing SarkarQnA API...")
    test_api()
    print("\n✅ Testing completed!")

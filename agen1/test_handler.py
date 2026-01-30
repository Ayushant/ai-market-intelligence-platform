#!/usr/bin/env python3
"""
Local testing script for AgentCore handler
Test the agent without deploying to AWS
"""

import json
import os
from dotenv import load_dotenv
from agentcore_handler import handler

# Load environment from .env.agentcore
load_dotenv('.env.agentcore')

def test_basic_research():
    """Test 1: Basic research request"""
    print("\n" + "="*60)
    print("TEST 1: Basic Research Request")
    print("="*60)
    
    test_event = {
        "topic": "Quantum Computing"
    }
    
    print(f"Input: {json.dumps(test_event, indent=2)}")
    
    try:
        result = handler(test_event, None)
        print(f"\nStatus Code: {result.get('statusCode')}")
        body = json.loads(result.get('body', '{}'))
        print(f"Success: {body.get('success')}")
        if body.get('success'):
            report = body.get('report')
            if isinstance(report, dict):
                print(f"Report Title: {report.get('title', 'N/A')}")
                print(f"Sections: {len(report.get('sections', []))}")
        else:
            print(f"Error: {body.get('error')}")
    except Exception as e:
        print(f"Exception: {str(e)}")

def test_missing_topic():
    """Test 2: Missing topic parameter"""
    print("\n" + "="*60)
    print("TEST 2: Missing Topic (Error Handling)")
    print("="*60)
    
    test_event = {}
    
    print(f"Input: {json.dumps(test_event, indent=2)}")
    
    result = handler(test_event, None)
    print(f"\nStatus Code: {result.get('statusCode')}")
    body = json.loads(result.get('body', '{}'))
    print(f"Error: {body.get('error')}")
    
    if result.get('statusCode') == 400:
        print("✓ Test passed: Correctly handled missing parameter")
    else:
        print("✗ Test failed: Should return 400 status code")

def test_different_topics():
    """Test 3: Multiple different topics"""
    print("\n" + "="*60)
    print("TEST 3: Multiple Topics")
    print("="*60)
    
    topics = [
        "Artificial Intelligence",
        "Blockchain Technology",
        "Edge Computing"
    ]
    
    for topic in topics:
        print(f"\n→ Testing topic: {topic}")
        test_event = {"topic": topic}
        
        try:
            result = handler(test_event, None)
            status = result.get('statusCode')
            body = json.loads(result.get('body', '{}'))
            success = body.get('success')
            
            if status == 200 and success:
                print(f"  ✓ Success")
            else:
                print(f"  ✗ Failed - Status: {status}")
        except Exception as e:
            print(f"  ✗ Exception: {str(e)[:100]}")

def test_performance():
    """Test 4: Measure response time"""
    print("\n" + "="*60)
    print("TEST 4: Performance Measurement")
    print("="*60)
    
    import time
    
    test_event = {"topic": "5G Networks"}
    
    print("Starting timer...")
    start_time = time.time()
    
    try:
        result = handler(test_event, None)
        elapsed_time = time.time() - start_time
        
        print(f"Execution time: {elapsed_time:.2f} seconds")
        
        body = json.loads(result.get('body', '{}'))
        if body.get('success'):
            print("✓ Request completed successfully")
        else:
            print(f"✗ Request failed: {body.get('error')}")
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"Failed after {elapsed_time:.2f} seconds")
        print(f"Error: {str(e)[:200]}")

if __name__ == "__main__":
    print("\n" + "🚀 "*10)
    print("AgentCore Handler Test Suite")
    print("🚀 "*10)
    
    # Check if .env.agentcore exists
    if not os.path.exists('.env.agentcore'):
        print("\n⚠️  WARNING: .env.agentcore not found!")
        print("Create it with your API keys before testing.\n")
        exit(1)
    
    # Run tests
    try:
        test_basic_research()
        test_missing_topic()
        # test_different_topics()  # Uncomment to test multiple topics
        # test_performance()       # Uncomment to measure performance
        
    except KeyboardInterrupt:
        print("\n\n⛔ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
    
    print("\n" + "="*60)
    print("Test suite completed!")
    print("="*60)

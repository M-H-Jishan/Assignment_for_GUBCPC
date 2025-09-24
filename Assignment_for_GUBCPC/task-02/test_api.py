#!/usr/bin/env python3
"""
Test script for the Solved Problems Tracker API
Run this script to test all API endpoints
"""

import requests
import json
import time

BASE_URL = 'http://localhost:5000'

def test_api():
    print("🧪 Testing Solved Problems Tracker API")
    print("=" * 50)
    
    # Test data
    test_problems = [
        {
            "user_id": "alice",
            "problem_title": "Two Sum",
            "problem_url": "https://leetcode.com/problems/two-sum/",
            "difficulty": "Easy",
            "platform": "LeetCode",
            "notes": "Used hash map for O(n) solution"
        },
        {
            "user_id": "alice",
            "problem_title": "Valid Parentheses",
            "problem_url": "https://leetcode.com/problems/valid-parentheses/",
            "difficulty": "Easy",
            "platform": "LeetCode",
            "notes": "Stack-based approach"
        },
        {
            "user_id": "bob",
            "problem_title": "Binary Search",
            "problem_url": "https://leetcode.com/problems/binary-search/",
            "difficulty": "Easy",
            "platform": "LeetCode",
            "notes": "Classic binary search implementation"
        }
    ]
    
    try:
        # Test 1: API Documentation
        print("1️⃣ Testing API Documentation (GET /)")
        response = requests.get(f'{BASE_URL}/')
        if response.status_code == 200:
            print("✅ API documentation endpoint working")
            print(f"   Message: {response.json()['message']}")
        else:
            print(f"❌ API documentation failed: {response.status_code}")
        print()
        
        # Test 2: Store problems
        print("2️⃣ Testing Store Problems (POST /solve)")
        for i, problem in enumerate(test_problems, 1):
            response = requests.post(f'{BASE_URL}/solve', json=problem)
            if response.status_code == 201:
                print(f"✅ Problem {i} stored successfully")
                print(f"   Title: {problem['problem_title']}")
                print(f"   User: {problem['user_id']}")
            else:
                print(f"❌ Failed to store problem {i}: {response.status_code}")
                print(f"   Error: {response.text}")
        print()
        
        # Test 3: Get problems for Alice
        print("3️⃣ Testing Get Problems for Alice (GET /solves/alice)")
        response = requests.get(f'{BASE_URL}/solves/alice')
        if response.status_code == 200:
            data = response.json()
            print("✅ Successfully retrieved Alice's problems")
            print(f"   Total solved: {data['total_solved']}")
            print(f"   Problems: {len(data['problems'])}")
            for problem in data['problems']:
                print(f"   - {problem['problem_title']} ({problem['difficulty']})")
        else:
            print(f"❌ Failed to get Alice's problems: {response.status_code}")
        print()
        
        # Test 4: Get problems for Bob
        print("4️⃣ Testing Get Problems for Bob (GET /solves/bob)")
        response = requests.get(f'{BASE_URL}/solves/bob')
        if response.status_code == 200:
            data = response.json()
            print("✅ Successfully retrieved Bob's problems")
            print(f"   Total solved: {data['total_solved']}")
            print(f"   Problems: {len(data['problems'])}")
            for problem in data['problems']:
                print(f"   - {problem['problem_title']} ({problem['difficulty']})")
        else:
            print(f"❌ Failed to get Bob's problems: {response.status_code}")
        print()
        
        # Test 5: Get all problems
        print("5️⃣ Testing Get All Problems (GET /solves)")
        response = requests.get(f'{BASE_URL}/solves')
        if response.status_code == 200:
            data = response.json()
            print("✅ Successfully retrieved all problems")
            print(f"   Total problems: {data['total_problems']}")
        else:
            print(f"❌ Failed to get all problems: {response.status_code}")
        print()
        
        # Test 6: Get user statistics
        print("6️⃣ Testing User Statistics (GET /stats/alice)")
        response = requests.get(f'{BASE_URL}/stats/alice')
        if response.status_code == 200:
            data = response.json()
            print("✅ Successfully retrieved Alice's statistics")
            print(f"   Total solved: {data['total_solved']}")
            print(f"   Difficulty breakdown: {data['difficulty_breakdown']}")
            print(f"   Platform breakdown: {data['platform_breakdown']}")
        else:
            print(f"❌ Failed to get Alice's statistics: {response.status_code}")
        print()
        
        # Test 7: Error handling - missing fields
        print("7️⃣ Testing Error Handling (POST /solve with missing fields)")
        invalid_problem = {"user_id": "test"}  # Missing problem_title
        response = requests.post(f'{BASE_URL}/solve', json=invalid_problem)
        if response.status_code == 400:
            print("✅ Error handling working correctly")
            print(f"   Error message: {response.json()['error']}")
        else:
            print(f"❌ Error handling failed: {response.status_code}")
        print()
        
        # Test 8: Non-existent user
        print("8️⃣ Testing Non-existent User (GET /solves/nonexistent)")
        response = requests.get(f'{BASE_URL}/solves/nonexistent')
        if response.status_code == 200:
            data = response.json()
            print("✅ Non-existent user handled correctly")
            print(f"   Total solved: {data['total_solved']}")
            print(f"   Problems: {len(data['problems'])}")
        else:
            print(f"❌ Non-existent user test failed: {response.status_code}")
        
        print("\n" + "=" * 50)
        print("🎉 API Testing Complete!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask server is running on localhost:5000")
        print("   Run: python app.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == '__main__':
    test_api()

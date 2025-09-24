#!/usr/bin/env python3
"""
Test script for Redis caching functionality in the Solved Problems Tracker API
Run this script to test cache behavior
"""

import requests
import json
import time

BASE_URL = 'http://localhost:5000'

def test_caching():
    print("🧪 Testing Redis Caching Functionality")
    print("=" * 50)
    
    try:
        # Test 1: Check cache status
        print("1️⃣ Testing Cache Status (GET /cache/status)")
        response = requests.get(f'{BASE_URL}/cache/status')
        if response.status_code == 200:
            data = response.json()
            print("✅ Cache status retrieved successfully")
            print(f"   Redis Available: {data.get('redis_available')}")
            if data.get('redis_available'):
                print(f"   Redis Version: {data.get('redis_version')}")
                print(f"   Total Keys: {data.get('total_keys')}")
                print(f"   Cache TTL: {data.get('cache_ttl')} seconds")
            else:
                print(f"   Message: {data.get('message')}")
        else:
            print(f"❌ Cache status check failed: {response.status_code}")
        print()
        
        # Test 2: Clear any existing cache for test user
        test_user = "cache_test_user"
        print(f"2️⃣ Clearing existing cache for {test_user}")
        response = requests.delete(f'{BASE_URL}/cache/{test_user}')
        if response.status_code == 200:
            data = response.json()
            print("✅ Cache cleared successfully")
            print(f"   Keys deleted: {data.get('keys_deleted', 0)}")
        print()
        
        # Test 3: Add a test problem
        print("3️⃣ Adding test problem")
        test_problem = {
            "user_id": test_user,
            "problem_title": "Cache Test Problem",
            "problem_url": "https://example.com/problem",
            "difficulty": "Easy",
            "platform": "TestPlatform",
            "notes": "Testing cache functionality"
        }
        
        response = requests.post(f'{BASE_URL}/solve', json=test_problem)
        if response.status_code == 201:
            print("✅ Test problem added successfully")
        else:
            print(f"❌ Failed to add test problem: {response.status_code}")
            print(f"   Error: {response.text}")
        print()
        
        # Test 4: First request (should be from API, not cache)
        print("4️⃣ First request - should be from API")
        start_time = time.time()
        response = requests.get(f'{BASE_URL}/solves/{test_user}')
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print("✅ First request successful")
            print(f"   Source: {data.get('source')}")
            print(f"   Total solved: {data.get('total_solved')}")
            print(f"   Response time: {(end_time - start_time)*1000:.2f}ms")
            
            if data.get('source') == 'api':
                print("✅ Correctly served from API (not cache)")
            else:
                print("⚠️  Expected source to be 'api'")
        else:
            print(f"❌ First request failed: {response.status_code}")
        print()
        
        # Test 5: Second request (should be from cache)
        print("5️⃣ Second request - should be from cache")
        start_time = time.time()
        response = requests.get(f'{BASE_URL}/solves/{test_user}')
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Second request successful")
            print(f"   Source: {data.get('source')}")
            print(f"   Total solved: {data.get('total_solved')}")
            print(f"   Response time: {(end_time - start_time)*1000:.2f}ms")
            print(f"   Cached at: {data.get('cached_at')}")
            
            if data.get('source') == 'cache':
                print("✅ Correctly served from cache")
            else:
                print("⚠️  Expected source to be 'cache'")
        else:
            print(f"❌ Second request failed: {response.status_code}")
        print()
        
        # Test 6: Add another problem (should invalidate cache)
        print("6️⃣ Adding another problem (should invalidate cache)")
        test_problem2 = {
            "user_id": test_user,
            "problem_title": "Cache Invalidation Test",
            "problem_url": "https://example.com/problem2",
            "difficulty": "Medium",
            "platform": "TestPlatform",
            "notes": "Testing cache invalidation"
        }
        
        response = requests.post(f'{BASE_URL}/solve', json=test_problem2)
        if response.status_code == 201:
            print("✅ Second test problem added successfully")
        else:
            print(f"❌ Failed to add second test problem: {response.status_code}")
        print()
        
        # Test 7: Request after cache invalidation (should be from API again)
        print("7️⃣ Request after adding problem - should be from API (cache invalidated)")
        start_time = time.time()
        response = requests.get(f'{BASE_URL}/solves/{test_user}')
        end_time = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Request after invalidation successful")
            print(f"   Source: {data.get('source')}")
            print(f"   Total solved: {data.get('total_solved')}")
            print(f"   Response time: {(end_time - start_time)*1000:.2f}ms")
            
            if data.get('source') == 'api':
                print("✅ Correctly served from API after cache invalidation")
                if data.get('total_solved') == 2:
                    print("✅ Cache invalidation working - shows updated count")
                else:
                    print("⚠️  Expected total_solved to be 2")
            else:
                print("⚠️  Expected source to be 'api' after cache invalidation")
        else:
            print(f"❌ Request after invalidation failed: {response.status_code}")
        print()
        
        # Test 8: Performance comparison
        print("8️⃣ Performance comparison (multiple requests)")
        
        # Clear cache first
        requests.delete(f'{BASE_URL}/cache/{test_user}')
        
        # First request (API)
        start_time = time.time()
        response = requests.get(f'{BASE_URL}/solves/{test_user}')
        api_time = time.time() - start_time
        
        # Second request (Cache)
        start_time = time.time()
        response = requests.get(f'{BASE_URL}/solves/{test_user}')
        cache_time = time.time() - start_time
        
        print(f"   API response time: {api_time*1000:.2f}ms")
        print(f"   Cache response time: {cache_time*1000:.2f}ms")
        
        if cache_time < api_time:
            print("✅ Cache is faster than API")
            speedup = (api_time - cache_time) / api_time * 100
            print(f"   Cache speedup: {speedup:.1f}%")
        else:
            print("⚠️  Cache should be faster than API")
        print()
        
        # Test 9: Non-existent user (should not be cached)
        print("9️⃣ Testing non-existent user")
        response = requests.get(f'{BASE_URL}/solves/nonexistent_user')
        if response.status_code == 200:
            data = response.json()
            print("✅ Non-existent user handled correctly")
            print(f"   Source: {data.get('source')}")
            print(f"   Total solved: {data.get('total_solved')}")
        print()
        
        # Cleanup
        print("🧹 Cleaning up test data")
        requests.delete(f'{BASE_URL}/cache/{test_user}')
        print("✅ Test cache cleared")
        
        print("\n" + "=" * 50)
        print("🎉 Redis Caching Tests Complete!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the Flask server is running on localhost:5000")
        print("   Run: python app.py")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == '__main__':
    test_caching()

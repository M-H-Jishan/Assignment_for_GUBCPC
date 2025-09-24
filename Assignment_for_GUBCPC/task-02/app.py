from flask import Flask, request, jsonify
from datetime import datetime
import json
import os
import redis
import logging

app = Flask(__name__)

# In-memory storage for solved problems
# In production, you would use a proper database
solved_problems = []

# File-based persistence (optional)
DATA_FILE = 'solved_problems.json'

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1 hour default

# Initialize Redis connection
try:
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5
    )
    # Test connection
    redis_client.ping()
    REDIS_AVAILABLE = True
    print("✅ Redis connection established")
except (redis.ConnectionError, redis.TimeoutError) as e:
    redis_client = None
    REDIS_AVAILABLE = False
    print(f"⚠️  Redis not available: {e}")
    print("📝 API will work without caching")

def load_data():
    """Load data from file if it exists"""
    global solved_problems
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                solved_problems = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            solved_problems = []

def save_data():
    """Save data to file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(solved_problems, f, indent=2)

def get_cache_key(user_id):
    """Generate Redis cache key for user"""
    return f"solved_problems:{user_id}"

def get_from_cache(user_id):
    """Get user's solved problems from Redis cache"""
    if not REDIS_AVAILABLE:
        return None
    
    try:
        cache_key = get_cache_key(user_id)
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
    except (redis.RedisError, json.JSONDecodeError) as e:
        print(f"Cache read error: {e}")
    
    return None

def set_cache(user_id, data):
    """Store user's solved problems in Redis cache"""
    if not REDIS_AVAILABLE:
        return False
    
    try:
        cache_key = get_cache_key(user_id)
        redis_client.setex(
            cache_key, 
            CACHE_TTL, 
            json.dumps(data, default=str)
        )
        return True
    except (redis.RedisError, json.JSONEncodeError) as e:
        print(f"Cache write error: {e}")
        return False

def invalidate_cache(user_id):
    """Remove user's data from cache when new problem is added"""
    if not REDIS_AVAILABLE:
        return
    
    try:
        cache_key = get_cache_key(user_id)
        redis_client.delete(cache_key)
    except redis.RedisError as e:
        print(f"Cache invalidation error: {e}")

# Load existing data on startup
load_data()

@app.route('/solve', methods=['POST'])
def store_solved_problem():
    """
    Store a solved problem
    Expected JSON payload:
    {
        "user_id": "string",
        "problem_title": "string",
        "problem_url": "string (optional)",
        "difficulty": "string (optional)",
        "platform": "string (optional)",
        "notes": "string (optional)"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'user_id' not in data or 'problem_title' not in data:
            return jsonify({
                'error': 'Missing required fields: user_id and problem_title'
            }), 400
        
        # Create solved problem entry
        solved_problem = {
            'id': len(solved_problems) + 1,
            'user_id': data['user_id'],
            'problem_title': data['problem_title'],
            'problem_url': data.get('problem_url', ''),
            'difficulty': data.get('difficulty', ''),
            'platform': data.get('platform', ''),
            'notes': data.get('notes', ''),
            'solved_at': datetime.now().isoformat()
        }
        
        # Add to storage
        solved_problems.append(solved_problem)
        
        # Save to file
        save_data()
        
        # Invalidate cache for this user
        invalidate_cache(data['user_id'])
        
        return jsonify({
            'message': 'Problem solved successfully recorded!',
            'problem': solved_problem
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/solves/<user_id>', methods=['GET'])
def get_solved_problems(user_id):
    """
    Get all solved problems for a specific user
    Returns the problems and total count with caching support
    """
    try:
        # First, try to get from cache
        cached_data = get_from_cache(user_id)
        if cached_data:
            return jsonify({
                'user_id': user_id,
                'total_solved': cached_data['total_solved'],
                'problems': cached_data['problems'],
                'source': 'cache',
                'cached_at': cached_data.get('cached_at')
            }), 200
        
        # If not in cache, fetch from data source
        user_problems = [
            problem for problem in solved_problems 
            if problem['user_id'] == user_id
        ]
        
        # Sort by solved_at timestamp (most recent first)
        user_problems.sort(key=lambda x: x['solved_at'], reverse=True)
        
        # Prepare response data
        response_data = {
            'total_solved': len(user_problems),
            'problems': user_problems,
            'cached_at': datetime.now().isoformat()
        }
        
        # Store in cache for future requests
        set_cache(user_id, response_data)
        
        return jsonify({
            'user_id': user_id,
            'total_solved': len(user_problems),
            'problems': user_problems,
            'source': 'api'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/solves', methods=['GET'])
def get_all_solved_problems():
    """
    Get all solved problems (bonus endpoint)
    """
    try:
        return jsonify({
            'total_problems': len(solved_problems),
            'problems': solved_problems
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/stats/<user_id>', methods=['GET'])
def get_user_stats(user_id):
    """
    Get statistics for a specific user (bonus endpoint)
    """
    try:
        user_problems = [
            problem for problem in solved_problems 
            if problem['user_id'] == user_id
        ]
        
        # Calculate statistics
        total_solved = len(user_problems)
        
        # Count by difficulty
        difficulty_stats = {}
        platform_stats = {}
        
        for problem in user_problems:
            difficulty = problem.get('difficulty', 'Unknown')
            platform = problem.get('platform', 'Unknown')
            
            difficulty_stats[difficulty] = difficulty_stats.get(difficulty, 0) + 1
            platform_stats[platform] = platform_stats.get(platform, 0) + 1
        
        return jsonify({
            'user_id': user_id,
            'total_solved': total_solved,
            'difficulty_breakdown': difficulty_stats,
            'platform_breakdown': platform_stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/', methods=['GET'])
def home():
    """
    API documentation endpoint
    """
    return jsonify({
        'message': 'Solved Problems Tracker API',
        'version': '1.0',
        'endpoints': {
            'POST /solve': 'Store a solved problem',
            'GET /solves/<user_id>': 'Get all solved problems for a user (with Redis caching)',
            'GET /solves': 'Get all solved problems',
            'GET /stats/<user_id>': 'Get user statistics',
            'GET /cache/status': 'Check Redis cache status',
            'DELETE /cache/<user_id>': 'Clear cache for specific user',
            'GET /': 'API documentation'
        },
        'caching': {
            'redis_available': REDIS_AVAILABLE,
            'cache_ttl': f'{CACHE_TTL} seconds',
            'redis_host': REDIS_HOST,
            'redis_port': REDIS_PORT
        },
        'example_usage': {
            'store_problem': {
                'method': 'POST',
                'url': '/solve',
                'body': {
                    'user_id': 'john_doe',
                    'problem_title': 'Two Sum',
                    'problem_url': 'https://leetcode.com/problems/two-sum/',
                    'difficulty': 'Easy',
                    'platform': 'LeetCode',
                    'notes': 'Used hash map approach'
                }
            },
            'get_problems': {
                'method': 'GET',
                'url': '/solves/john_doe'
            }
        }
    })

# Additional cache management endpoints
@app.route('/cache/status', methods=['GET'])
def cache_status():
    """
    Check Redis cache status and statistics
    """
    try:
        if not REDIS_AVAILABLE:
            return jsonify({
                'redis_available': False,
                'message': 'Redis is not available'
            }), 200
        
        # Get Redis info
        info = redis_client.info()
        
        return jsonify({
            'redis_available': True,
            'redis_version': info.get('redis_version'),
            'connected_clients': info.get('connected_clients'),
            'used_memory_human': info.get('used_memory_human'),
            'total_keys': redis_client.dbsize(),
            'cache_ttl': CACHE_TTL,
            'uptime_in_seconds': info.get('uptime_in_seconds')
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error checking cache status: {str(e)}'
        }), 500

@app.route('/cache/<user_id>', methods=['DELETE'])
def clear_user_cache(user_id):
    """
    Clear cache for a specific user
    """
    try:
        if not REDIS_AVAILABLE:
            return jsonify({
                'message': 'Redis is not available, no cache to clear'
            }), 200
        
        cache_key = get_cache_key(user_id)
        deleted = redis_client.delete(cache_key)
        
        return jsonify({
            'message': f'Cache cleared for user: {user_id}',
            'keys_deleted': deleted
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Error clearing cache: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Solved Problems Tracker API

A simple REST API built with Python Flask to track solved programming problems.

## Features

- Store solved problems with detailed information
- Retrieve all solved problems for a specific user
- Get total count of solved problems
- **Redis Caching**: Fast response times with intelligent cache management
- File-based data persistence
- User statistics and analytics
- Cache invalidation on data updates
- Graceful fallback when Redis is unavailable

## API Endpoints

### 1. Store a Solved Problem
**POST** `/solve`

Store a new solved problem for a user.

**Request Body:**
```json
{
    "user_id": "john_doe",
    "problem_title": "Two Sum",
    "problem_url": "https://leetcode.com/problems/two-sum/",
    "difficulty": "Easy",
    "platform": "LeetCode",
    "notes": "Used hash map approach"
}
```

**Response:**
```json
{
    "message": "Problem solved successfully recorded!",
    "problem": {
        "id": 1,
        "user_id": "john_doe",
        "problem_title": "Two Sum",
        "problem_url": "https://leetcode.com/problems/two-sum/",
        "difficulty": "Easy",
        "platform": "LeetCode",
        "notes": "Used hash map approach",
        "solved_at": "2024-01-15T10:30:00.123456"
    }
}
```

### 2. Get Solved Problems for a User
**GET** `/solves/<user_id>`

Retrieve all solved problems for a specific user with total count.

**Response:**
```json
{
    "user_id": "john_doe",
    "total_solved": 5,
    "problems": [
        {
            "id": 1,
            "user_id": "john_doe",
            "problem_title": "Two Sum",
            "problem_url": "https://leetcode.com/problems/two-sum/",
            "difficulty": "Easy",
            "platform": "LeetCode",
            "notes": "Used hash map approach",
            "solved_at": "2024-01-15T10:30:00.123456"
        }
    ]
}
```

### 3. Bonus Endpoints

#### Get All Problems
**GET** `/solves`

#### Get User Statistics
**GET** `/stats/<user_id>`

#### API Documentation
**GET** `/`

## Installation & Setup

1. **Install Redis (if using caching):**
   ```bash
   # Windows (using Chocolatey)
   choco install redis-64
   
   # macOS (using Homebrew)
   brew install redis
   
   # Ubuntu/Debian
   sudo apt-get install redis-server
   
   # Start Redis server
   redis-server
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **The API will be available at:**
   ```
   http://localhost:5000
   ```

### Redis Configuration

The API supports Redis caching with the following environment variables:

- `REDIS_HOST`: Redis server host (default: localhost)
- `REDIS_PORT`: Redis server port (default: 6379)
- `REDIS_DB`: Redis database number (default: 0)
- `CACHE_TTL`: Cache time-to-live in seconds (default: 3600)

Example:
```bash
export REDIS_HOST=localhost
export REDIS_PORT=6379
export CACHE_TTL=1800
python app.py
```

## Usage Examples

### Using curl

**Store a problem:**
```bash
curl -X POST http://localhost:5000/solve \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "john_doe",
    "problem_title": "Two Sum",
    "problem_url": "https://leetcode.com/problems/two-sum/",
    "difficulty": "Easy",
    "platform": "LeetCode",
    "notes": "Used hash map approach"
  }'
```

**Get user's solved problems:**
```bash
curl http://localhost:5000/solves/john_doe
```

**Check cache status:**
```bash
curl http://localhost:5000/cache/status
```

**Clear user cache:**
```bash
curl -X DELETE http://localhost:5000/cache/john_doe
```

### Using Python requests

```python
import requests

# Store a problem
response = requests.post('http://localhost:5000/solve', json={
    'user_id': 'john_doe',
    'problem_title': 'Two Sum',
    'problem_url': 'https://leetcode.com/problems/two-sum/',
    'difficulty': 'Easy',
    'platform': 'LeetCode',
    'notes': 'Used hash map approach'
})

# Get solved problems
response = requests.get('http://localhost:5000/solves/john_doe')
data = response.json()
print(f"Total solved: {data['total_solved']}")
```

## Data Storage

The API uses file-based persistence with `solved_problems.json`. In production, consider using a proper database like PostgreSQL or MongoDB.

## Error Handling

The API includes comprehensive error handling and returns appropriate HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request (missing required fields)
- `500` - Internal Server Error

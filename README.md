# Assignment for GUBCPC

This repository contains three programming tasks demonstrating frontend and backend development skills.

## Project Structure

```
Assignment_for_GUBCPC/
├── task-01/          # Personal Info Card (Frontend - Very Easy)
├── task-02/          # Solved Problems Tracker API (Backend - Easy)
├── task-03/          # Codeforces Contests Tracker (Frontend - Hard)
└── README.md         # This file
```

## Tasks Overview

### Task 1: Personal Info Card (Frontend - Very Easy)
**Location:** `task-01/`

A responsive personal information card built with HTML, CSS, and JavaScript.

**Features:**
- Displays name, university, and favorite programming language
- Hover effects with card animation
- Dark mode toggle functionality
- Responsive design for all devices
- Uses actual profile image as avatar

**Technologies:** HTML5, CSS3, JavaScript (ES6+)

### Task 2: Solved Problems Tracker API (Backend - Easy)
**Location:** `task-02/`

A REST API for tracking solved programming problems with Redis caching.

**Features:**
- Store solved problems with detailed information
- Retrieve problems by user ID
- Redis caching for improved performance
- Cache invalidation on data updates
- File-based data persistence
- Comprehensive API documentation

**Technologies:** Python, Flask, Redis

**Endpoints:**
- `POST /solve` - Store a solved problem
- `GET /solves/:user_id` - Get user's solved problems (cached)
- `GET /cache/status` - Check Redis cache status
- `DELETE /cache/:user_id` - Clear user cache

### Task 3: Codeforces Contests Tracker (Frontend - Hard)
**Location:** `task-03/`

A modern web application that fetches and displays programming contests from Codeforces API.

**Features:**
- Real-time contest data from Codeforces API
- Live countdown timers for upcoming contests
- Browser notifications for contest reminders
- Filter contests (upcoming, past, all)
- Responsive design with modern UI
- Dark mode support
- Error handling and loading states

**Technologies:** HTML5, CSS3, JavaScript (ES6+), Codeforces API

## Getting Started

### Prerequisites
- Python 3.7+ (for task-02)
- Redis server (optional, for caching in task-02)
- Modern web browser (for task-01 and task-03)

### Running the Projects

#### Task 1 - Personal Info Card
```bash
cd task-01
# Open index.html in your browser
```

#### Task 2 - API Server
```bash
cd task-02
pip install -r requirements.txt
python app.py
# API available at http://localhost:5000
```

#### Task 3 - Contests Tracker
```bash
cd task-03
# Open index.html in your browser
```

## Testing

Each task includes comprehensive testing:

- **Task 1:** Manual testing through browser interaction
- **Task 2:** Automated test suite (`test_api.py`, `test_cache.py`)
- **Task 3:** Manual testing with live API integration

## Features Implemented

### Core Requirements ✅
- [x] Personal info card with hover effects
- [x] REST API with GET/POST endpoints
- [x] Codeforces API integration with live countdown
- [x] Browser notifications for reminders
- [x] Responsive design for all tasks

### Bonus Features ✅
- [x] Dark mode toggle (Task 1)
- [x] Redis caching with performance optimization (Task 2)
- [x] Past contests filter and statistics (Task 3)
- [x] Comprehensive error handling
- [x] Modern UI/UX design

## Technical Highlights

- **Performance:** Redis caching reduces API response times significantly
- **Reliability:** Graceful fallback when external services are unavailable
- **User Experience:** Smooth animations, loading states, and error messages
- **Code Quality:** Clean, well-documented, and maintainable code
- **Testing:** Comprehensive test suites for backend functionality

## Author

**Moynul Hasan Jishan**
Dept. of Software Engineering
Green University of Bangladesh

## License

This project is created for educational purposes as part of GUBCPC assignment.

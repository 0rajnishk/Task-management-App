# Flask with Celery & Redis

## Overview
This project integrates **Flask**, **Celery**, and **Redis** to handle scheduled tasks, queued tasks, and caching efficiently. Celery is used for background task execution, Redis serves as both a message broker and a caching system.

## Features
✅ **Queued Tasks** - Process long-running tasks asynchronously using Celery workers.
✅ **Scheduled Tasks** - Run periodic tasks like report generation.
✅ **Caching with Redis** - Store frequently accessed data in Redis to reduce database queries.
✅ **JWT Authentication** - Secure API endpoints using JSON Web Tokens (JWT).

## Technologies Used
- **Flask** - Web framework for Python
- **Celery** - Distributed task queue
- **Redis** - Message broker & caching solution
- **Flask-JWT-Extended** - Authentication & authorization
- **Flask-RESTful** - API development

## Installation & Setup

### Prerequisites
Make sure you have **Python 3.x**, **Redis**, and **Celery** installed.

### 1. Clone the Repository
```bash
git clone <repo-url>
cd <project-folder>
```

### 2. Create a Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Start Redis Server
```bash
redis-server
```

### 4. Start Celery Worker
```bash
celery -A app.celery worker --loglevel=info
```

### 5. Run Flask Application
```bash
python app.py
```

## API Endpoints

### Authentication
- **POST** `/register` - Register a new user
- **POST** `/login` - Login and obtain JWT token

### Task Management
- **GET** `/tasks` - Retrieve all tasks (admin/manager only)
- **POST** `/tasks` - Create a new task (manager/admin)
- **PUT** `/task/<task_id>` - Update task details (manager/admin)
- **DELETE** `/task/<task_id>` - Delete a task (admin only)

### Task Execution
- **POST** `/process-task/<task_id>` - Queue a long-running task
- **POST** `/trigger-report` - Schedule report generation task

### Caching
- **GET** `/stats` - Fetch task statistics (data is cached in Redis)

## Running Celery Tasks
### Queued Task Example
When calling `/process-task/<task_id>`, a background task is scheduled to process the task asynchronously.
```python
@celery.task
def process_long_task(task_id):
    # Process task here
```

### Scheduled Task Example
The `/trigger-report` endpoint schedules a task that runs every hour and caches the result in Redis.
```python
@celery.task
def scheduled_report():
    total_tasks = Task.query.count()
    redis_client.set("task_report", str(report), ex=3600)  # Cache for 1 hour
```

## License
This project is open-source and available under the MIT License.


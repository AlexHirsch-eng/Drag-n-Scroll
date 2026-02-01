# Drag'n'Scroll Backend

Django REST API for Chinese Learning Application with SRS (Spaced Repetition System).

## Features

- **User Authentication**: JWT-based authentication with Djoser
- **Course Management**: Structured courses with days, lessons, and steps
- **Vocabulary System**: Chinese words with translations, audio, and HSK levels
- **Grammar Rules**: Explanations with examples in Russian and Kazakh
- **SRS Algorithm**: SuperMemo SM-2 implementation for spaced repetition
- **Progress Tracking**: Session progress, XP system, and streaks

## Tech Stack

- Django 4.2
- Django REST Framework
- Djoser (authentication)
- PostgreSQL
- SimpleJWT (JWT tokens)

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Virtual environment (venv or conda)

### 2. Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your configuration
# Make sure to set SECRET_KEY and database credentials
```

### 4. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 5. Run Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/refresh/` - Refresh JWT token

### User
- `GET /api/user/me/` - Get current user profile
- `PATCH /api/user/me/` - Update user profile
- `GET /api/user/profile/` - Get user profile details

### Learning
- `GET /api/learning/current-session/` - Get current lesson
- `GET /api/learning/lesson-steps/?lesson_id=<id>` - Get lesson steps
- `POST /api/learning/submit-step/` - Submit step answer
- `POST /api/learning/finish-session/` - Finish session

### Vocabulary
- `GET /api/vocab/words/` - List all words
- `GET /api/vocab/words/<id>/` - Get word details
- `GET /api/vocab/my-words/` - Get user's words with progress
- `GET /api/vocab/grammar/` - List grammar rules

### SRS (Spaced Repetition)
- `GET /api/learning/srs/review-batch/` - Get words for review
- `POST /api/learning/srs/submit-review/` - Submit review results
- `GET /api/learning/srs/due-count/` - Get due word count
- `GET /api/learning/srs/stats/` - Get SRS statistics

## SRS Algorithm

This project implements the SuperMemo SM-2 algorithm:

- **Quality Ratings (0-5)**:
  - 5: Perfect response (< 3 sec)
  - 4: Correct response (3-10 sec)
  - 3: Correct response (> 10 sec or with difficulty)
  - 2: Incorrect but remembered with hint
  - 1: Incorrect but recognized correct answer
  - 0: Complete failure

- **Intervals**:
  - Level 0: New (not yet learned)
  - Level 1: 1 day
  - Level 2: 6 days
  - Level 3+: Previous interval × ease factor

## Data Models

See the project architecture document for detailed model relationships.

## Development

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Access admin panel at http://localhost:8000/admin
```

## Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Set `SECRET_KEY` to a strong random value
3. Configure `ALLOWED_HOSTS`
4. Set up a production database (PostgreSQL)
5. Configure static file serving (e.g., Whitenoise, S3)
6. Set up a WSGI server (e.g., Gunicorn)
7. Configure reverse proxy (e.g., Nginx)

## License

MIT

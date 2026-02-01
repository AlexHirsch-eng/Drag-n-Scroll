# Backend Setup and Data Population Guide

This guide explains how to set up the backend and populate it with realistic sample data.

## Prerequisites

- Python 3.13+
- Django 4.2+
- SQLite (default) or PostgreSQL/MySQL

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Populate Data with Realistic Content

The backend now includes management commands to populate the database with realistic sample data.

#### Populate Chat Data (Users, Conversations, Stories)

```bash
python manage.py populate_chats
```

This creates:
- **6 realistic users** with profiles
- **7 chat rooms** (5 direct messages, 2 group chats)
- **75+ messages** with realistic Chinese learning conversations
- **6 stories** with views and reactions

Example conversations include:
- HSK exam preparation discussions
- Grammar help sessions
- Vocabulary practice groups
- Cultural exchange discussions
- Study group coordination

#### Populate Video Data (Videos, Comments, Interactions)

```bash
python manage.py populate_videos
```

This creates:
- **5 content creators**
- **7 video categories** (Vocabulary, Grammar, Culture, Listening, Speaking, Writing, Tips)
- **18 diverse videos** covering:
  - HSK 3 vocabulary lessons
  - Grammar explanations (把 structure, passive voice, etc.)
  - Cultural content (Chinese New Year, tea culture, table manners)
  - Listening practice exercises
  - Speaking and pronunciation tips
  - Writing and character lessons
  - Learning strategies and tips
- **61 hashtags** for content discovery
- **User interactions** (views, likes, comments, bookmarks, shares)

## What Gets Created

### Chat System

**Users:**
- alex_chen - Learning Chinese for 2 years
- emma_wang - HSK 4 student
- david_liu - Loves Chinese culture
- sophia_zhang - Native speaker helping learners
- michael_wu - Business Chinese learner
- lisa_ma - Preparing for HSK 5

**Chat Rooms:**
1. **Direct Message**: Alex & Emma - HSK 4 exam discussion
2. **Direct Message**: David & Sophia - Grammar help session
3. **Direct Message**: Michael & Lisa - Business Chinese practice
4. **Group Chat**: Chinese Study Group - Multi-user study coordination
5. **Direct Message**: Alex & Sophia - Pronunciation practice
6. **Direct Message**: Emma & Lisa - Chinese drama discussion
7. **Group Chat**: Beijing expats - Local life discussions

**Sample Conversations Include:**
- Real Chinese language exchanges
- Learning tips and advice
- Grammar explanations
- Cultural discussions
- Study coordination
- Resource sharing

### Video System

**Categories:**
- 📚 Vocabulary - Word lessons and HSK vocabulary
- 📝 Grammar - Sentence structures and patterns
- 🏮 Culture - Traditions and customs
- 🎧 Listening - Comprehension exercises
- 🗣️ Speaking - Pronunciation and conversation
- ✍️ Writing - Characters and stroke order
- 💡 Tips - Learning strategies and motivation

**Video Examples:**
1. HSK 3 Unit 1: Daily Routine Vocabulary
2. Food Vocabulary in Chinese
3. Master the 把 (bǎ) Structure
4. Chinese New Year Traditions
5. Tone Practice: The Four Tones
6. Stroke Order Basics
7. How I Memorize 50 Words Daily
8. ... and 10 more!

Each video includes:
- Title and description (Chinese & English)
- Relevant hashtags
- Lesson information
- Realistic view counts
- User comments
- Likes and interactions

## Running the Server

```bash
python manage.py runserver
```

The backend will be available at: `http://localhost:8000`

## API Endpoints

Once populated, you can access:

### Chat API
- `GET /api/chat/rooms/` - List all chat rooms
- `GET /api/chat/rooms/{id}/messages/` - Get chat messages
- `POST /api/chat/rooms/{id}/messages/` - Send message
- `GET /api/chat/stories/` - Get stories

### Video API
- `GET /api/videos/feed/` - Get video feed
- `GET /api/videos/{id}/` - Get video details
- `POST /api/videos/{id}/like/` - Like video
- `GET /api/videos/{id}/comments/` - Get video comments

## Reset Data

To clear all data and start fresh:

```bash
# SQLite (default)
rm backend/db.sqlite3
python manage.py migrate
python manage.py populate_chats
python manage.py populate_videos

# Or with Python
python manage.py flush
python manage.py populate_chats
python manage.py populate_videos
```

## Manual Data Creation

You can also use the Python shell to create data:

```bash
python manage.py shell
```

```python
from chat_app.management.commands.populate_chats import Command
cmd = Command()
cmd.handle()

from video_app.management.commands.populate_videos import Command
cmd = Command()
cmd.handle()
```

## Troubleshooting

### Command Not Found

If you get "Unknown command: populate_chats":
```bash
# Make sure management commands are properly set up
find . -type d -name "management"
```

You should see:
- `chat_app/management/commands/populate_chats.py`
- `video_app/management/commands/populate_videos.py`

### Encoding Issues on Windows

The commands handle Windows console encoding automatically. If you see encoding errors:
```bash
# Set console to UTF-8
chcp 65001
python manage.py populate_chats
```

### Database Locked (SQLite)

If you get "database is locked" errors:
```bash
# Stop any running Django servers
# Delete the lock file
rm backend/db.sqlite3-wal
rm backend/db.sqlite3-shm
```

## Frontend Integration

The frontend is already set up to use this data:

1. **TikTok-style Video Player**: Located at `frontend/src/views/VideosView.vue`
   - Vertical swipe to switch videos
   - Touch and mouse wheel support
   - Like, comment, share functionality
   - Video feed with categories

2. **Chat Interface**: Located at `frontend/src/views/ChatView.vue`
   - Direct and group messages
   - Stories row
   - Real-time messaging UI
   - Typing indicators
   - Search and filters

## Next Steps

1. **Start the backend**: `python manage.py runserver`
2. **Start the frontend**: `cd ../frontend && npm run dev`
3. **Open the app**: Navigate to `http://localhost:5173`
4. **Explore the content**:
   - Check out the Videos section to see TikTok-style video switching
   - Browse the Chat section to see realistic conversations
   - Try interacting with the content (likes, comments, messages)

## Production Considerations

For production deployment:

1. Change database to PostgreSQL
2. Set up proper media file storage (S3, CloudFront)
3. Configure CORS properly
4. Add authentication middleware
5. Set up Redis for WebSocket connections
6. Configure email backend for notifications
7. Add rate limiting
8. Enable proper logging

## Support

For issues or questions:
- Check the Django documentation: https://docs.djangoproject.com/
- Review the API documentation in the code
- Check existing issues in the project repository

---

**Enjoy exploring the fully populated Chinese learning platform! 加油！**

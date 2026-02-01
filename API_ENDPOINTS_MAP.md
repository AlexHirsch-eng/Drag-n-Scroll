# 📡 ПОЛНАЯ КАРТА API ENDPOINTS

## Backend → Frontend Сопоставление

### ✅ Authentication Endpoints
**Backend**: `/api/auth/`
- `POST /api/auth/users/` - Register
- `POST /api/auth/jwt/create/` - Login
- `POST /api/auth/jwt/refresh/` - Refresh token
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/users/me/` - Get current user

**Frontend**: `frontend/src/api/auth.ts` ✅

---

### ✅ User Profile Endpoints
**Backend**: `/api/user/`
- `GET /api/user/profile/` - Get profile
- `PATCH /api/user/profile/` - Update profile
- `GET /api/user/me/` - Get user detail

**Frontend**: `frontend/src/api/auth.ts` ✅

---

### ✅ Learning Endpoints
**Backend**: `/api/learning/`
- `GET /api/learning/main-screen/` - Main screen data
- `POST /api/learning/start/` - Start session
- `GET /api/learning/step/<id>/` - Get step data
- `POST /api/learning/complete/` - Complete session
- `POST /api/learning/submit/step-1/` - Submit Step 1
- `POST /api/learning/submit/step-2/` - Submit Step 2
- `POST /api/learning/submit/step-3/` - Submit Step 3
- `POST /api/learning/submit/step-4/` - Submit Step 4
- `POST /api/learning/submit/step-5/` - Submit Step 5

**Frontend**: `frontend/src/api/learning.ts` ✅

---

### ✅ Vocab Endpoints
**Backend**: `/api/vocab/`
- `GET /api/vocab/words/` - List words
- `POST /api/vocab/words/` - Create word
- `GET /api/vocab/my-words/` - My words
- `POST /api/vocab/my-words/` - Add to my words
- `GET /api/vocab/grammar/` - Grammar rules
- `GET /api/vocab/history/` - Review history

**Frontend**: `frontend/src/api/vocab.ts` ✅

---

### ✅ Course Endpoints
**Backend**: `/api/course/`
- `GET /api/course/courses/` - List courses
- `GET /api/course/days/` - List course days
- `GET /api/course/lessons/` - List lessons
- `GET /api/course/steps/` - Lesson steps

**Frontend**: Нужно проверить (возможно не используется)

---

### ✅ Video Endpoints
**Backend**: `/api/video/`
- `GET /api/video/videos/` - List videos
- `POST /api/video/videos/` - Create video
- `GET /api/video/categories/` - Categories
- `GET /api/video/videos/<id>/comments/` - Comments
- `POST /api/video/comments/<id>/like/` - Like comment
- `POST /api/video/comments/<id>/translate/` - Translate
- `GET /api/video/users/<id>/feed/` - User feed
- `POST /api/video/users/<id>/follow/` - Follow user
- `POST /api/video/admin/import-videos/` - Import videos
- `GET /api/video/categories-list/` - Categories list

**Frontend**: `frontend/src/api/video.ts` ✅

---

### ✅ Chat Endpoints
**Backend**: `/api/chat/`
- `GET /api/chat/rooms/` - Chat rooms
- `POST /api/chat/rooms/` - Create room
- `GET /api/chat/messages/` - Messages
- `POST /api/chat/messages/` - Send message
- `GET /api/chat/users/suggested/` - Suggested users
- `POST /api/chat/rooms/<id>/read/` - Mark read
- `POST /api/chat/messages/<id>/translate/` - Translate
- `GET /api/chat/stories/` - Stories
- `POST /api/chat/stories/<id>/react/` - React

**Frontend**: `frontend/src/api/chat.ts` ✅

---

## 🎯 Frontend Routes

| Path | Component | Auth Required |
|------|-----------|---------------|
| `/` | HomeView | ❌ |
| `/login` | LoginView | ❌ |
| `/register` | RegisterView | ❌ |
| `/learn` | LearnView | ✅ |
| `/session` | SessionView | ✅ |
| `/lesson` | LessonView | ✅ |
| `/review` | ReviewView | ✅ |
| `/profile` | ProfileView (own) | ✅ |
| `/profile/:id` | ProfileView (other) | ✅ |
| `/vocab` | VocabView | ✅ |
| `/stats` | StatsView | ✅ |
| `/videos` | VideosView | ✅ |
| `/chat` | ChatView | ✅ |

---

## 🔧 НЕИСПРАВЛЕННЫЕ ПРОБЛЕМЫ

### ⚠️ Потенциальные проблемы:

1. **Course API endpoints** - не используются во фронтенде
2. **Vocab API** - есть frontend но нужно проверить используется ли
3. **Review view** - есть route но нужно проверить view компонент

Далее: Тестирование всех страниц...

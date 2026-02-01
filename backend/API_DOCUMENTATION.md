# Drag'n'Scroll API Documentation

## Полная документация всех API endpoints

---

## 🔐 Authentication API (Djoser)

### POST /api/auth/users/
**Регистрация нового пользователя**

Request:
```json
{
  "username": "student123",
  "email": "student@example.com",
  "password": "securepass123",
  "learning_language": "RU"  // или "KZ"
}
```

Response (201):
```json
{
  "id": 1,
  "username": "student123",
  "email": "student@example.com"
}
```

### POST /api/auth/jwt/create/
**Логин (получение JWT токена)**

Request:
```json
{
  "username": "student123",
  "password": "securepass123"
}
```

Response (200):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### POST /api/auth/jwt/refresh/
**Обновление access токена**

Request:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

Response (200):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### POST /api/auth/jwt/verify/
**Проверка валидности токена**

Request:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

Response (200): Token is valid

---

## 👤 User API

### GET /api/user/me/
**Получить данные пользователя**

Headers:
```
Authorization: Bearer <access_token>
```

Response (200):
```json
{
  "id": 1,
  "username": "student123",
  "email": "student@example.com",
  "profile": {
    "learning_language": "RU",
    "current_hsk_level": 1,
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z"
  },
  "progress": {
    "current_day": 8,
    "current_lesson": 5,
    "current_step": 1,
    "total_xp": 1250,
    "streak_days": 5,
    "last_study_date": "2025-01-27",
    "completed_days": [1, 2, 3, 4, 5, 6, 7]
  }
}
```

### PATCH /api/user/me/
**Обновить данные пользователя**

Request:
```json
{
  "email": "newemail@example.com"
}
```

Response (200): Updated user data

### GET /api/user/profile/
**Получить настройки профиля**

Response (200):
```json
{
  "learning_language": "RU",
  "current_hsk_level": 1,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

### PATCH /api/user/profile/
**Обновить настройки профиля**

Request:
```json
{
  "learning_language": "KZ",
  "current_hsk_level": 2
}
```

---

## 📚 Learning API

### GET /api/learning/current-session/
**Получить текущий урок/сессию**

Response (200):
```json
{
  "course_day": {
    "id": 8,
    "day_number": 8,
    "title": "Базовые глаголы",
    "estimated_minutes": 15
  },
  "lesson": {
    "id": 5,
    "lesson_type": "MIXED",
    "title": "Глаголы действия",
    "hsk_level": 1
  },
  "session": {
    "id": 45,
    "started_at": "2025-01-27T10:00:00Z",
    "current_step_index": 0,
    "steps_completed": 0,
    "steps_correct": 0,
    "xp_earned": 0
  },
  "next_step": {
    "step_number": 1,
    "step_type": "VOCAB_INTRO",
    "title": "Новые слова",
    "estimated_minutes": 2
  }
}
```

### GET /api/learning/lesson-steps/?lesson_id=5
**Получить все шаги урока**

Query Parameters:
- `lesson_id` (required): ID урока

Response (200):
```json
{
  "lesson": {
    "id": 5,
    "title": "Глаголы действия",
    "total_steps": 5
  },
  "steps": [
    {
      "id": 1,
      "order": 1,
      "step_type": "VOCAB_INTRO",
      "title": "Новые слова",
      "estimated_minutes": 2,
      "content": {
        "words": [
          {
            "id": 101,
            "hanzi": "喝",
            "pinyin": "hē",
            "translation_ru": "пить",
            "translation_kz": "ішу",
            "audio_url": "/media/audio/he.mp3"
          }
        ]
      }
    },
    {
      "id": 2,
      "order": 2,
      "step_type": "VOCAB_RECOGNIZE",
      "title": "Выбери перевод",
      "estimated_minutes": 1,
      "content": {
        "question": {
          "hanzi": "喝",
          "pinyin": "hē"
        },
        "options": [
          {"id": "a", "text": "пить / ішу"},
          {"id": "b", "text": "есть / жему"}
        ],
        "correct_answer": "a"
      }
    }
  ]
}
```

### POST /api/learning/submit-step/
**Отправить ответ на шаг**

Request:
```json
{
  "session_id": 45,
  "step_id": 2,
  "user_answer": {
    "selected_option": "a"
  },
  "time_spent_seconds": 5
}
```

Response (200):
```json
{
  "is_correct": true,
  "xp_earned": 10,
  "streak_updated": true,
  "next_step": {
    "step_id": 3,
    "step_type": "GRAMMAR_INTRO",
    "title": "Грамматика"
  },
  "session_progress": {
    "steps_completed": 1,
    "steps_correct": 1,
    "xp_earned": 10
  }
}
```

### POST /api/learning/finish-session/
**Завершить сессию**

Request:
```json
{
  "session_id": 45
}
```

Response (200):
```json
{
  "session_completed": true,
  "xp_earned": 50,
  "steps_completed": 5,
  "steps_correct": 4,
  "accuracy": 0.8,
  "time_spent_minutes": 12,
  "next_lesson": {
    "day_number": 9,
    "lesson_id": 6,
    "title": "Путешествие"
  }
}
```

---

## 🔄 SRS API

### GET /api/learning/srs/review-batch/?batch_size=10
**Получить слова на повторение**

Query Parameters:
- `batch_size` (optional): Размер батча, default 10
- `hsk_level` (optional): Фильтр по HSK уровню

Response (200):
```json
{
  "batch_id": "rev_12345",
  "words": [
    {
      "id": 101,
      "hanzi": "喝",
      "pinyin": "hē",
      "translation_ru": "пить",
      "translation_kz": "ішу",
      "audio_url": "/media/audio/he.mp3",
      "srs_level": 2,
      "total_reviews": 5
    }
  ],
  "total_due": 25,
  "batch_number": 1,
  "total_batches": 3
}
```

### POST /api/learning/srs/submit-review/
**Отправить результаты повторения**

Request:
```json
{
  "batch_id": "rev_12345",
  "reviews": [
    {
      "word_id": 101,
      "quality": 5,
      "time_spent_seconds": 3
    },
    {
      "word_id": 102,
      "quality": 3,
      "time_spent_seconds": 8
    }
  ]
}
```

Response (200):
```json
{
  "reviews_processed": 2,
  "words_updated": [
    {
      "word_id": 101,
      "old_srs_level": 2,
      "new_srs_level": 3,
      "old_interval": 3,
      "new_interval": 7,
      "next_review_date": "2025-02-03T10:00:00Z"
    }
  ],
  "xp_earned": 20
}
```

### GET /api/learning/srs/due-count/
**Количество слов на повторение**

Response (200):
```json
{
  "due_now": 25,
  "due_today": 15,
  "due_this_week": 80,
  "total_learning": 120,
  "total_mastered": 45
}
```

### GET /api/learning/srs/stats/
**SRS статистика**

Response (200):
```json
{
  "total_words": 165,
  "by_srs_level": {
    "0": 45,
    "1": 30,
    "2": 25,
    "3": 20,
    "4": 15,
    "5": 10,
    "6": 10,
    "7": 5,
    "8": 5
  },
  "retention_rate": 0.85,
  "avg_reviews_per_word": 4.2,
  "streak_days": 5,
  "upcoming_reviews": [
    {"date": "2025-01-28", "count": 12},
    {"date": "2025-01-29", "count": 8},
    {"date": "2025-01-30", "count": 15}
  ]
}
```

---

## 📖 Vocab API

### GET /api/vocab/words/
**Все слова (с фильтрами)**

Query Parameters:
- `hsk_level`: 1-6
- `part_of_speech`: noun/verb/adjective/etc
- `search`: поиск по hanzi/pinyin/translation
- `ordering`: hanzi/pinyin/frequency_rank/hsk_level

Response (200):
```json
{
  "count": 1000,
  "next": "/api/vocab/words/?page=2",
  "results": [
    {
      "id": 101,
      "hanzi": "喝",
      "pinyin": "hē",
      "translation_ru": "пить",
      "translation_kz": "ішу",
      "audio_url": "/media/audio/he.mp3",
      "hsk_level": 1,
      "frequency_rank": 245,
      "part_of_speech": "verb"
    }
  ]
}
```

### GET /api/vocab/words/{id}/
**Детали слова**

Response (200):
```json
{
  "id": 101,
  "hanzi": "喝",
  "pinyin": "hē",
  "translation_ru": "пить",
  "translation_kz": "ішу",
  "audio_url": "/media/audio/he.mp3",
  "hsk_level": 1,
  "frequency_rank": 245,
  "part_of_speech": "verb",
  "user_progress": {
    "srs_level": 2,
    "interval_days": 3,
    "next_review_date": "2025-01-30T10:00:00Z",
    "total_reviews": 5,
    "correct_reviews": 4,
    "accuracy": 0.8
  },
  "related_words": [
    {
      "id": 102,
      "hanzi": "茶",
      "pinyin": "chá"
    }
  ]
}
```

### GET /api/vocab/my-words/
**Слова пользователя с прогрессом**

Query Parameters:
- `word__hsk_level`: Фильтр по HSK уровню
- `srs_level`: Фильтр по SRS уровню (0-8)

Response (200):
```json
{
  "count": 45,
  "results": [
    {
      "word": {
        "id": 101,
        "hanzi": "喝",
        "pinyin": "hē",
        "translation_ru": "пить"
      },
      "progress": {
        "srs_level": 2,
        "interval_days": 3,
        "next_review_date": "2025-01-30T10:00:00Z",
        "total_reviews": 5,
        "correct_reviews": 4,
        "accuracy": 0.8
      }
    }
  ]
}
```

### GET /api/vocab/grammar/
**Грамматические правила**

Query Parameters:
- `hsk_level`: Фильтр по HSK уровню
- `search`: Поиск по title/pattern/explanation

Response (200):
```json
{
  "count": 20,
  "results": [
    {
      "id": 1,
      "title": "把-конструкция",
      "pattern": "Subject + 把 + Object + Verb",
      "explanation_ru": "Конструкция для...",
      "explanation_kz": "Құрылым...",
      "hsk_level": 1,
      "examples": [
        {
          "sentence_hanzi": "我把茶喝了。",
          "sentence_pinyin": "Wǒ bǎ chá hē le.",
          "translation_ru": "Я выпил чай.",
          "translation_kz": "Мен шайді іштім.",
          "audio_url": "/media/audio/example.mp3"
        }
      ]
    }
  ]
}
```

---

## 🎓 Course API

### GET /api/course/courses/
**Все курсы**

Query Parameters:
- `hsk_level`: Фильтр по HSK уровню

Response (200):
```json
{
  "count": 6,
  "results": [
    {
      "id": 1,
      "title": "HSK 1 Complete Course",
      "hsk_level": 1,
      "total_days": 30,
      "is_active": true
    }
  ]
}
```

### GET /api/course/days/
**Дни курса**

Query Parameters:
- `course_id`: ID курса
- `day_number`: Номер дня

### GET /api/course/lessons/
**Уроки**

Query Parameters:
- `course_day_id`: ID дня курса

### GET /api/course/steps/
**Шаги уроков**

Query Parameters:
- `lesson_id`: ID урока

---

## 📊 Models Description

### User Models:
- **User**: Расширенная модель пользователя
- **UserProfile**: Настройки обучения (язык, HSK уровень)
- **UserCourseProgress**: Прогресс по курсу (текущий день, XP, streak)

### Course Models:
- **Course**: Основной курс (HSK 1-6)
- **CourseDay**: День в курсе (30 дней на курс)
- **Lesson**: Урок в дне (vocab/grammar/mixed)
- **LessonStep**: Шаг урока (vocab intro, recognize, etc.)

### Vocab Models:
- **Word**: Китайское слово с переводами
- **WordProgress**: SRS прогресс для каждого слова
- **GrammarRule**: Грамматические правила
- **GrammarExample**: Примеры для правил
- **ReviewHistory**: История повторений

### Learning Models:
- **SessionProgress**: Прогресс сессии обучения
- **LessonStepProgress**: Прогресс по отдельным шагам
- **SRSBatch**: Батчи для SRS повторений

---

## ⚠️ Error Codes

- **400**: Bad Request - Неверные данные
- **401**: Unauthorized - Токен истёк или неверный
- **404**: Not Found - Ресурс не найден
- **500**: Internal Server Error - Ошибка сервера

---

## 🔒 Authentication

Все API endpoints (кроме `/api/auth/`) требуют заголовок:

```
Authorization: Bearer <access_token>
```

Получить токен можно через `/api/auth/jwt/create/` при логине.

---

## 📝 Пример использования

### 1. Регистрация и логин:
```
POST /api/auth/users/ - создать пользователя
POST /api/auth/jwt/create/ - получить токен
```

### 2. Начать обучение:
```
GET /api/learning/current-session/ - получить текущий урок
GET /api/learning/lesson-steps/?lesson_id=1 - получить шаги
```

### 3. Проходить урок:
```
POST /api/learning/submit-step/ - отправить ответ
POST /api/learning/finish-session/ - завершить урок
```

### 4. Повторение слов:
```
GET /api/learning/srs/review-batch/ - получить слова
POST /api/learning/srs/submit-review/ - отправить результаты
```

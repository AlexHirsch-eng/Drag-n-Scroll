"""
Script to create minimal course data for the learning system.
Run this on Render via: "Render Shell" -> "Python Shell"
"""

from course.models import Course, CourseDay
from vocab.models import Word, GrammarRule
from core.models import User

def create_minimal_course():
    """Create a minimal HSK 1 course with 1 day"""

    # Check if course already exists
    existing = Course.objects.filter(hsk_level=1).first()
    if existing:
        print(f"Course HSK 1 already exists: {existing.title}")
        return existing

    # Create HSK 1 Course
    course = Course.objects.create(
        hsk_level=1,
        title="HSK 1 - Уровень 1",
        description="Начальный курс китайского языка",
        is_active=True
    )
    print(f"✓ Created course: {course.title}")

    # Create Day 1
    course_day = CourseDay.objects.create(
        course=course,
        day_number=1,
        title="День 1: Приветствие",
        description="Первые слова и фразы",
        estimated_minutes=15
    )
    print(f"✓ Created course day: {course_day.title}")

    # Add some basic words to Day 1
    words_data = [
        {
            "hanzi": "你好",
            "pinyin": "nǐ hǎo",
            "translation_ru": "Привет",
            "translation_kz": "Сәлем",
            "hsk_level": 1
        },
        {
            "hanzi": "我",
            "pinyin": "wǒ",
            "translation_ru": "Я",
            "translation_kz": "Мен",
            "hsk_level": 1
        },
        {
            "hanzi": "你",
            "pinyin": "nǐ",
            "translation_ru": "Ты",
            "translation_kz": "Сен",
            "hsk_level": 1
        },
        {
            "hanzi": "谢谢",
            "pinyin": "xiè xie",
            "translation_ru": "Спасибо",
            "translation_kz": "Рахмет",
            "hsk_level": 1
        },
        {
            "hanzi": "再见",
            "pinyin": "zài jiàn",
            "translation_ru": "До свидания",
            "translation_kz": "Сау бол",
            "hsk_level": 1
        }
    ]

    for word_data in words_data:
        word, created = Word.objects.get_or_create(
            hanzi=word_data["hanzi"],
            defaults={
                **word_data,
                "audio_url": ""
            }
        )
        course_day.new_words.add(word)
        print(f"  ✓ Added word: {word.hanzi} - {word.translation_ru}")

    print(f"\n✅ Course HSK 1 created successfully!")
    print(f"   Total words: {course_day.new_words.count()}")
    return course

if __name__ == "__main__":
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    print("=== Creating Minimal Course Data ===\n")
    course = create_minimal_course()
    print(f"\nCourse ID: {course.id}")
    print(f"Users can now access: /api/learning/main-screen/?hsk=1")

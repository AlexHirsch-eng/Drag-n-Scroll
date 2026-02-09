from django.core.management.base import BaseCommand
from course.models import Course, CourseDay
from vocab.models import Word


class Command(BaseCommand):
    help = 'Create minimal demo course with sample data'

    def handle(self, *args, **options):
        self.stdout.write("=== Creating Demo Course ===\n")

        # Check if course already exists
        existing = Course.objects.filter(hsk_level=1).first()
        if existing:
            self.stdout.write(self.style.WARNING(f"Course HSK 1 already exists"))
            return

        # Create HSK 1 Course
        course = Course.objects.create(
            hsk_level=1,
            title="HSK 1 - Начальный уровень",
            description="Базовый курс китайского языка для начинающих",
            is_active=True
        )
        self.stdout.write(self.style.SUCCESS(f"✓ Created course: {course.title}"))

        # Create Day 1
        course_day = CourseDay.objects.create(
            course=course,
            day_number=1,
            title="Урок 1: Приветствие и знакомство",
            description="Научимся здороваться и представляться",
            estimated_minutes=15
        )
        self.stdout.write(self.style.SUCCESS(f"✓ Created lesson: {course_day.title}"))

        # Add basic words
        words_data = [
            {"hanzi": "你好", "pinyin": "nǐ hǎo", "ru": "Привет", "kz": "Сәлем"},
            {"hanzi": "我", "pinyin": "wǒ", "ru": "Я", "kz": "Мен"},
            {"hanzi": "你", "pinyin": "nǐ", "ru": "Ты", "kz": "Сен"},
            {"hanzi": "谢谢", "pinyin": "xiè xie", "ru": "Спасибо", "kz": "Рахмет"},
            {"hanzi": "再见", "pinyin": "zài jiàn", "ru": "До свидания", "kz": "Сау бол"},
        ]

        for w in words_data:
            word, _ = Word.objects.get_or_create(
                hanzi=w["hanzi"],
                defaults={
                    "pinyin": w["pinyin"],
                    "translation_ru": w["ru"],
                    "translation_kz": w["kz"],
                    "hsk_level": 1
                }
            )
            course_day.new_words.add(word)
            self.stdout.write(f"  ✓ {w['hanzi']} - {w['ru']}")

        self.stdout.write(self.style.SUCCESS(f"\n✅ Demo course created successfully!"))
        self.stdout.write(f"   Course ID: {course.id}")
        self.stdout.write(f"   Total words: {course_day.new_words.count()}")

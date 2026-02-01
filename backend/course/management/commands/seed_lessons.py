"""
Management command to create lesson steps with actual content
"""
from django.core.management.base import BaseCommand
from course.models import Course, CourseDay, Lesson, LessonStep
from vocab.models import Word


class Command(BaseCommand):
    help = 'Create lesson steps with content'

    def handle(self, *args, **options):
        self.stdout.write('Creating lesson steps...')

        # Get all words
        words = list(Word.objects.filter(hsk_level=1))
        if not words:
            self.stdout.write(self.style.ERROR('No words found! Run seed_vocab first.'))
            return

        # Get Day 1 Lesson
        course_day = CourseDay.objects.filter(day_number=1).first()
        lesson = Lesson.objects.filter(course_day=course_day).first()

        if not lesson:
            self.stdout.write(self.style.ERROR('Lesson not found!'))
            return

        # Clear existing steps
        LessonStep.objects.filter(lesson=lesson).delete()

        # Step 1: Vocab Introduction (5 words)
        step1 = LessonStep.objects.create(
            lesson=lesson,
            step_type='VOCAB_INTRO',
            order=1,
            title='New Words',
            estimated_minutes=2,
            content={'description': 'Learn these new Chinese words!'}
        )
        step1.words.set(words[:5])

        # Step 2: Vocab Recognize (quiz)
        step2 = LessonStep.objects.create(
            lesson=lesson,
            step_type='VOCAB_RECOGNIZE',
            order=2,
            title='Choose Translation',
            estimated_minutes=1,
            content={
                'question': {
                    'hanzi': words[0].hanzi,
                    'pinyin': words[0].pinyin,
                    'audio_url': words[0].audio_url or ''
                },
                'options': [
                    {'id': 'a', 'text': f'{words[0].translation_ru} / {words[0].translation_kz}'},
                    {'id': 'b', 'text': f'{words[1].translation_ru} / {words[1].translation_kz}'},
                    {'id': 'c', 'text': f'{words[2].translation_ru} / {words[2].translation_kz}'},
                    {'id': 'd', 'text': f'{words[3].translation_ru} / {words[3].translation_kz}'}
                ],
                'correct_answer': 'a'
            }
        )

        # Step 3: Vocab Recognize (second word)
        step3 = LessonStep.objects.create(
            lesson=lesson,
            step_type='VOCAB_RECOGNIZE',
            order=3,
            title='Choose Translation',
            estimated_minutes=1,
            content={
                'question': {
                    'hanzi': words[1].hanzi,
                    'pinyin': words[1].pinyin,
                    'audio_url': words[1].audio_url or ''
                },
                'options': [
                    {'id': 'a', 'text': f'{words[2].translation_ru} / {words[2].translation_kz}'},
                    {'id': 'b', 'text': f'{words[1].translation_ru} / {words[1].translation_kz}'},
                    {'id': 'c', 'text': f'{words[3].translation_ru} / {words[3].translation_kz}'},
                    {'id': 'd', 'text': f'{words[4].translation_ru} / {words[4].translation_kz}'}
                ],
                'correct_answer': 'b'
            }
        )

        # Step 4: Vocab Recognize (third word)
        step4 = LessonStep.objects.create(
            lesson=lesson,
            step_type='VOCAB_RECOGNIZE',
            order=4,
            title='Choose Translation',
            estimated_minutes=1,
            content={
                'question': {
                    'hanzi': words[2].hanzi,
                    'pinyin': words[2].pinyin,
                    'audio_url': words[2].audio_url or ''
                },
                'options': [
                    {'id': 'a', 'text': f'{words[4].translation_ru} / {words[4].translation_kz}'},
                    {'id': 'b', 'text': f'{words[3].translation_ru} / {words[3].translation_kz}'},
                    {'id': 'c', 'text': f'{words[2].translation_ru} / {words[2].translation_kz}'},
                    {'id': 'd', 'text': f'{words[5].translation_ru} / {words[5].translation_kz}'}
                ],
                'correct_answer': 'c'
            }
        )

        # Step 5: Build Phrase
        step5 = LessonStep.objects.create(
            lesson=lesson,
            step_type='BUILD_PHRASE',
            order=5,
            title='Build the Phrase',
            estimated_minutes=2,
            content={
                'instruction_ru': 'Build the phrase: "I am Chinese"',
                'instruction_kz': 'Сөйлемді құрыңыз: "Мен қытаймын"',
                'target_hanzi': '我是中国人',
                'target_pinyin': 'Wǒ shì Zhōng guó rén',
                'options': [
                    {'id': 1, 'hanzi': '我', 'pinyin': 'wǒ'},
                    {'id': 2, 'hanzi': '是', 'pinyin': 'shì'},
                    {'id': 3, 'hanzi': '中国', 'pinyin': 'Zhōng guó'},
                    {'id': 4, 'hanzi': '人', 'pinyin': 'rén'}
                ],
                'correct_order': [1, 2, 3, 4]
            }
        )

        self.stdout.write(self.style.SUCCESS(f'Created 5 lesson steps for Day 1!'))

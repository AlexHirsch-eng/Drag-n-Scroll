"""
Create test data for Session A/B testing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Course, CourseDay
from vocab.models import Word, GrammarRule
from learning.models import Dialogue, WordArrangementExercise, GrammarTask
from django.contrib.auth import get_user_model

User = get_user_model()

# Get the first course and course days
course = Course.objects.first()
days = course.days.all()

print(f"Found {days.count()} course days")

# Assign words to course days if not already assigned
all_words = list(Word.objects.all())
print(f"Found {len(all_words)} words")

for i, day in enumerate(days):
    # Assign 5 words to each day
    start_idx = i * 5
    end_idx = start_idx + 5
    day_words = all_words[start_idx:end_idx]

    if day_words:
        day.new_words.set(day_words)
        print(f"  Assigned {len(day_words)} words to Day {day.day_number}")

    # Assign grammar rules to days
    all_rules = list(GrammarRule.objects.all())
    if all_rules:
        day.grammar_rules.set([all_rules[i % len(all_rules)]])
        print(f"  Assigned grammar rule to Day {day.day_number}")

# Clear existing test data
Dialogue.objects.all().delete()
WordArrangementExercise.objects.all().delete()
GrammarTask.objects.all().delete()

print("Cleared existing test data")

# Create test data for each day
for day in days:
    print(f"\nCreating data for Day {day.day_number}...")

    # Get some words from this day
    day_words = list(day.new_words.all()[:5])

    if not day_words:
        print(f"  No words found for Day {day.day_number}, skipping...")
        continue

    # Create Dialogue for Session A
    dialogue_a = Dialogue.objects.create(
        course_day=day,
        session_type='A',
        lines=[
            {
                'speaker': 'A',
                'hanzi': '你好',
                'pinyin': 'nǐ hǎo',
                'translation_ru': 'Привет',
                'translation_kz': 'Сәлем'
            },
            {
                'speaker': 'B',
                'hanzi': '你好吗？',
                'pinyin': 'nǐ hǎo ma?',
                'translation_ru': 'Как дела?',
                'translation_kz': 'Қалайсың?'
            }
        ],
        question_hanzi='你好吗？',
        question_pinyin='nǐ hǎo ma?',
        audio_url='',
        options=[
            {
                'hanzi': '我很好',
                'pinyin': 'wǒ hěn hǎo',
                'translation_ru': 'Я очень хорошо',
                'translation_kz': 'Мен жақсымын',
                'is_correct': True
            },
            {
                'hanzi': '我不知道',
                'pinyin': 'wǒ bù zhī dào',
                'translation_ru': 'Я не знаю',
                'translation_kz': 'Мен білмеймін',
                'is_correct': False
            },
            {
                'hanzi': '谢谢',
                'pinyin': 'xiè xie',
                'translation_ru': 'Спасибо',
                'translation_kz': 'Рахмет',
                'is_correct': False
            }
        ],
        explanation_ru='Правильный ответ: "我很好" (Я очень хорошо)',
        explanation_kz='Дұрыс жауап: "我很好" (Мен жақсымын)'
    )
    print(f"  [OK] Created Dialogue for Session A")

    # Create Dialogue for Session B
    dialogue_b = Dialogue.objects.create(
        course_day=day,
        session_type='B',
        lines=[
            {
                'speaker': 'A',
                'hanzi': '你叫什么名字？',
                'pinyin': 'nǐ jiào shén me míng zi?',
                'translation_ru': 'Как тебя зовут?',
                'translation_kz': 'Атың кім?'
            },
            {
                'speaker': 'B',
                'hanzi': '我叫李明',
                'pinyin': 'wǒ jiào Lǐ Míng',
                'translation_ru': 'Меня зовут Ли Мин',
                'translation_kz': 'Менің атым Ли Мин'
            }
        ],
        question_hanzi='你叫什么名字？',
        question_pinyin='nǐ jiào shén me míng zi?',
        audio_url='',
        options=[
            {
                'hanzi': '我叫李明',
                'pinyin': 'wǒ jiào Lǐ Míng',
                'translation_ru': 'Меня зовут Ли Мин',
                'translation_kz': 'Менің атым Ли Мин',
                'is_correct': True
            },
            {
                'hanzi': '我是学生',
                'pinyin': 'wǒ shì xué sheng',
                'translation_ru': 'Я студент',
                'translation_kz': 'Мен студент',
                'is_correct': False
            },
            {
                'hanzi': '再见',
                'pinyin': 'zài jiàn',
                'translation_ru': 'До свидания',
                'translation_kz': 'Сау бол',
                'is_correct': False
            }
        ],
        explanation_ru='Правильный ответ: "我叫李明" (Меня зовут Ли Мин)',
        explanation_kz='Дұрыс жауап: "我叫李明" (Менің атым Ли Мин)'
    )
    print(f"  [OK] Created Dialogue for Session B")

    # Create Word Arrangement for Session A
    if len(day_words) >= 2:
        word_arrangement_a = WordArrangementExercise.objects.create(
            course_day=day,
            session_type='A',
            target_hanzi='你好吗',
            target_pinyin='nǐ hǎo ma',
            target_translation_ru='Как дела?',
            target_translation_kz='Қалайсың?',
            hint_ru='Соберите приветствие',
            hint_kz='Сәлемдесуді жинаңыз',
            audio_url='',
            scrambled_words=[
                {'id': day_words[0].id, 'hanzi': '好', 'pinyin': 'hǎo'},
                {'id': day_words[1].id, 'hanzi': '你', 'pinyin': 'nǐ'},
                {'id': day_words[0].id, 'hanzi': '吗', 'pinyin': 'ma'}
            ]
        )
        print(f"  [OK] Created WordArrangement for Session A")

    # Create Word Arrangement for Session B
    if len(day_words) >= 2:
        word_arrangement_b = WordArrangementExercise.objects.create(
            course_day=day,
            session_type='B',
            target_hanzi='我是学生',
            target_pinyin='wǒ shì xué sheng',
            target_translation_ru='Я студент',
            target_translation_kz='Мен студент',
            hint_ru='Соберите предложение о профессии',
            hint_kz='Кәсіп туралы сөйлемді жинаңыз',
            audio_url='',
            scrambled_words=[
                {'id': day_words[0].id, 'hanzi': '我', 'pinyin': 'wǒ'},
                {'id': day_words[1].id, 'hanzi': '是', 'pinyin': 'shì'},
                {'id': day_words[0].id, 'hanzi': '学生', 'pinyin': 'xué sheng'}
            ]
        )
        print(f"  [OK] Created WordArrangement for Session B")

    # Create Grammar Tasks for Session A
    if day.grammar_rules.exists():
        grammar_rule = day.grammar_rules.first()

        grammar_task_a = GrammarTask.objects.create(
            course_day=day,
            session_type='A',
            grammar_rule=grammar_rule,
            task_prompt_ru='Постройте предложение: "Я студент"',
            task_prompt_kz='Сөйлем құрыңыз: "Мен студент"',
            components=[
                {
                    'id': day_words[0].id if day_words else 1,
                    'hanzi': '我',
                    'pinyin': 'wǒ',
                    'translation_ru': 'Я',
                    'translation_kz': 'Мен',
                    'type': 'pronoun'
                },
                {
                    'id': day_words[1].id if len(day_words) > 1 else 2,
                    'hanzi': '是',
                    'pinyin': 'shì',
                    'translation_ru': 'быть',
                    'translation_kz': 'болу',
                    'type': 'verb'
                },
                {
                    'id': day_words[2].id if len(day_words) > 2 else 3,
                    'hanzi': '学生',
                    'pinyin': 'xué sheng',
                    'translation_ru': 'студент',
                    'translation_kz': 'студент',
                    'type': 'noun'
                }
            ],
            correct_hanzi='我是学生',
            correct_pinyin='wǒ shì xué sheng',
            correct_translation_ru='Я студент',
            correct_translation_kz='Мен студент'
        )
        print(f"  [OK] Created GrammarTask for Session A")

        # Create Grammar Tasks for Session B
        grammar_task_b = GrammarTask.objects.create(
            course_day=day,
            session_type='B',
            grammar_rule=grammar_rule,
            task_prompt_ru='Постройте предложение: "Ты тоже студент"',
            task_prompt_kz='Сөйлем құрыңыз: "Сен де студент"',
            components=[
                {
                    'id': day_words[0].id if day_words else 1,
                    'hanzi': '你',
                    'pinyin': 'nǐ',
                    'translation_ru': 'ты',
                    'translation_kz': 'сен',
                    'type': 'pronoun'
                },
                {
                    'id': day_words[1].id if len(day_words) > 1 else 2,
                    'hanzi': '也',
                    'pinyin': 'yě',
                    'translation_ru': 'тоже',
                    'translation_kz': 'да',
                    'type': 'adverb'
                },
                {
                    'id': day_words[2].id if len(day_words) > 2 else 3,
                    'hanzi': '是',
                    'pinyin': 'shì',
                    'translation_ru': 'быть',
                    'translation_kz': 'болу',
                    'type': 'verb'
                },
                {
                    'id': day_words[3].id if len(day_words) > 3 else 4,
                    'hanzi': '学生',
                    'pinyin': 'xué sheng',
                    'translation_ru': 'студент',
                    'translation_kz': 'студент',
                    'type': 'noun'
                }
            ],
            correct_hanzi='你也是学生',
            correct_pinyin='nǐ yě shì xué sheng',
            correct_translation_ru='Ты тоже студент',
            correct_translation_kz='Сен де студент'
        )
        print(f"  [OK] Created GrammarTask for Session B")

print("\n=== Test Data Created Successfully ===")
print(f"Dialogues: {Dialogue.objects.count()}")
print(f"WordArrangementExercises: {WordArrangementExercise.objects.count()}")
print(f"GrammarTasks: {GrammarTask.objects.count()}")

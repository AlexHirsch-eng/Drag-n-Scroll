import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Lesson, LessonStep
from vocab.models import Word

# Get Lesson 2
lesson2 = Lesson.objects.filter(id=2).first()
if not lesson2:
    print('Lesson 2 not found!')
    exit(1)

print(f'Creating steps for Lesson 2: {lesson2.title}')

# Get words 6-10 for Lesson 2
words = Word.objects.filter(id__in=[6, 7, 8, 9, 10])
print(f'Using words: {list(words.values_list("id", flat=True))}')

# Step 1: Vocabulary Introduction
step1 = LessonStep.objects.create(
    lesson=lesson2,
    step_type='VOCAB_INTRO',
    title='New Words',
    order=1,
    estimated_minutes=5,
    content={
        'instruction': 'Learn these new words',
        'words_per_card': 5
    }
)
step1.words.set([6, 7, 8, 9, 10])
print(f'Created Step 1: VOCAB_INTRO with words {list(step1.words.values_list("id", flat=True))}')

# Step 2: Vocabulary Recognition (Word 6)
step2 = LessonStep.objects.create(
    lesson=lesson2,
    step_type='VOCAB_RECOGNIZE',
    title='Choose Translation',
    order=2,
    estimated_minutes=2,
    content={
        'word_id': 6,
        'question_type': 'hanzi_to_translation',
        'options': ['distractor_1', 'distractor_2', 'distractor_3']
    }
)
print(f'Created Step 2: VOCAB_RECOGNIZE')

# Step 3: Vocabulary Recognition (Word 7)
step3 = LessonStep.objects.create(
    lesson=lesson2,
    step_type='VOCAB_RECOGNIZE',
    title='Choose Translation',
    order=3,
    estimated_minutes=2,
    content={
        'word_id': 7,
        'question_type': 'hanzi_to_translation',
        'options': ['distractor_1', 'distractor_2', 'distractor_3']
    }
)
print(f'Created Step 3: VOCAB_RECOGNIZE')

# Step 4: Vocabulary Recognition (Word 8)
step4 = LessonStep.objects.create(
    lesson=lesson2,
    step_type='VOCAB_RECOGNIZE',
    title='Choose Translation',
    order=4,
    estimated_minutes=2,
    content={
        'word_id': 8,
        'question_type': 'hanzi_to_translation',
        'options': ['distractor_1', 'distractor_2', 'distractor_3']
    }
)
print(f'Created Step 4: VOCAB_RECOGNIZE')

# Step 5: Build Phrase
step5 = LessonStep.objects.create(
    lesson=lesson2,
    step_type='BUILD_PHRASE',
    title='Build the Phrase',
    order=5,
    estimated_minutes=3,
    content={
        'target_phrase': '',
        'words': [6, 7, 8]
    }
)
step5.words.set([6, 7, 8])
print(f'Created Step 5: BUILD_PHRASE')

print('\nDone! Lesson 2 now has 5 steps.')

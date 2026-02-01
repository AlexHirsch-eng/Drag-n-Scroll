import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import LessonStep

# Get all STEP_TYPES from model
print('STEP_TYPES in LessonStep model:')
step_types = [
    'VOCAB_INTRO',
    'VOCAB_RECOGNIZE',
    'VOCAB_MATCH',
    'GRAMMAR_INTRO',
    'BUILD_PHRASE',
    'FILL_BLANK',
    'SRS_REVIEW'
]
for st in step_types:
    print(f'  - {st}')

print('\nComponents in LessonView.vue:')
print('  - VOCAB_INTRO: VocabIntroCard')
print('  - VOCAB_RECOGNIZE: VocabRecognizeCard')
print('  - BUILD_PHRASE: BuildPhraseCard')
print('  - GRAMMAR_INTRO: GrammarIntroCard')
print('  - SRS_REVIEW: SRSReviewCard')

print('\nMissing components:')
missing = []
for st in step_types:
    has_component = st in ['VOCAB_INTRO', 'VOCAB_RECOGNIZE', 'BUILD_PHRASE', 'GRAMMAR_INTRO', 'SRS_REVIEW']
    if not has_component:
        missing.append(st)

if missing:
    for m in missing:
        print(f'  - {m}: No component')
else:
    print('  None - all step types have components!')

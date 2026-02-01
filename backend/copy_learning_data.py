"""
Copy learning data from HSK 1 to HSK 2-6
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Course, CourseDay
from learning.models import Dialogue, WordArrangementExercise, GrammarTask

def copy_learning_data():
    """Copy dialogues, arrangements, and grammar from HSK 1 to other levels"""

    # Get HSK 1 course
    hsk1_course = Course.objects.filter(hsk_level=1).first()
    if not hsk1_course:
        print('HSK 1 course not found!')
        return

    print(f'Copying data from HSK 1...\n')

    for target_level in range(2, 7):
        target_course = Course.objects.filter(hsk_level=target_level).first()
        if not target_course:
            print(f'HSK {target_level} course not found, skipping...')
            continue

        print(f'=== HSK {target_level} ===')

        # Copy dialogues
        for hsk1_day in hsk1_course.days.all():
            target_day = target_course.days.filter(day_number=hsk1_day.day_number).first()
            if not target_day:
                continue

            # Copy Session A dialogues
            for dialogue in hsk1_day.dialogues.filter(session_type='A'):
                Dialogue.objects.create(
                    course_day=target_day,
                    session_type='A',
                    lines=dialogue.lines,
                    question_hanzi=dialogue.question_hanzi,
                    question_pinyin=dialogue.question_pinyin,
                    question_translation_ru=dialogue.question_translation_ru,
                    question_translation_kz=dialogue.question_translation_kz,
                    audio_url=dialogue.audio_url,
                    options=dialogue.options,
                    explanation_ru=dialogue.explanation_ru,
                    explanation_kz=dialogue.explanation_kz,
                    order=dialogue.order
                )
            print(f'  - Copied {hsk1_day.dialogues.filter(session_type="A").count()} Session A dialogues for Day {hsk1_day.day_number}')

            # Copy Session B dialogues
            for dialogue in hsk1_day.dialogues.filter(session_type='B'):
                Dialogue.objects.create(
                    course_day=target_day,
                    session_type='B',
                    lines=dialogue.lines,
                    question_hanzi=dialogue.question_hanzi,
                    question_pinyin=dialogue.question_pinyin,
                    question_translation_ru=dialogue.question_translation_ru,
                    question_translation_kz=dialogue.question_translation_kz,
                    audio_url=dialogue.audio_url,
                    options=dialogue.options,
                    explanation_ru=dialogue.explanation_ru,
                    explanation_kz=dialogue.explanation_kz,
                    order=dialogue.order
                )

            # Copy arrangements
            for arrangement in hsk1_day.arrangement_exercises.filter(session_type='A'):
                WordArrangementExercise.objects.create(
                    course_day=target_day,
                    session_type='A',
                    target_hanzi=arrangement.target_hanzi,
                    target_pinyin=arrangement.target_pinyin,
                    target_translation_ru=arrangement.target_translation_ru,
                    target_translation_kz=arrangement.target_translation_kz,
                    audio_url=arrangement.audio_url,
                    scrambled_words=arrangement.scrambled_words,
                    hint_ru=arrangement.hint_ru,
                    hint_kz=arrangement.hint_kz,
                    order=arrangement.order
                )

            for arrangement in hsk1_day.arrangement_exercises.filter(session_type='B'):
                WordArrangementExercise.objects.create(
                    course_day=target_day,
                    session_type='B',
                    target_hanzi=arrangement.target_hanzi,
                    target_pinyin=arrangement.target_pinyin,
                    target_translation_ru=arrangement.target_translation_ru,
                    target_translation_kz=arrangement.target_translation_kz,
                    audio_url=arrangement.audio_url,
                    scrambled_words=arrangement.scrambled_words,
                    hint_ru=arrangement.hint_ru,
                    hint_kz=arrangement.hint_kz,
                    order=arrangement.order
                )

            # Copy grammar tasks
            for grammar in hsk1_day.grammar_tasks.filter(session_type='A'):
                GrammarTask.objects.create(
                    course_day=target_day,
                    session_type='A',
                    grammar_rule=grammar.grammar_rule,
                    task_prompt_ru=grammar.task_prompt_ru,
                    task_prompt_kz=grammar.task_prompt_kz,
                    components=grammar.components,
                    correct_hanzi=grammar.correct_hanzi,
                    correct_pinyin=grammar.correct_pinyin,
                    correct_translation_ru=grammar.correct_translation_ru,
                    correct_translation_kz=grammar.correct_translation_kz,
                    order=grammar.order
                )

            for grammar in hsk1_day.grammar_tasks.filter(session_type='B'):
                GrammarTask.objects.create(
                    course_day=target_day,
                    session_type='B',
                    grammar_rule=grammar.grammar_rule,
                    task_prompt_ru=grammar.task_prompt_ru,
                    task_prompt_kz=grammar.task_prompt_kz,
                    components=grammar.components,
                    correct_hanzi=grammar.correct_hanzi,
                    correct_pinyin=grammar.correct_pinyin,
                    correct_translation_ru=grammar.correct_translation_ru,
                    correct_translation_kz=grammar.correct_translation_kz,
                    order=grammar.order
                )

        print(f'  - All data copied for HSK {target_level}\n')

    print('All learning data copied successfully!')

if __name__ == '__main__':
    copy_learning_data()

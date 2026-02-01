import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from course.models import Course

# Get course
course = Course.objects.filter(hsk_level=1, is_active=True).first()
if course:
    print('Course:', course.title)
    print('Total days:', course.days.count())
    
    total_lessons = 0
    for day in course.days.all():
        lessons = day.lessons.count()
        total_lessons += lessons
        print(f'Day {day.day_number}: {lessons} lessons')
    
    print(f'Total lessons: {total_lessons}')

print('\n=== Course Completion Logic ===')
print('When all lessons completed:')
print('- Reset to Day 1, Lesson 1')
print('- Set course_completed = true')
print('- Show completion banner')
print('- Allow course repeat')

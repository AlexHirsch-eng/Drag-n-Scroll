import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import resolve

print("Testing URL resolution...")
try:
    match = resolve('/api/learning/main-screen/')
    print(f"OK URL resolved to: {match.func.__name__}")
    print(f"OK View name: {match.url_name}")
    print(f"OK Namespaces: {match.namespaces}")
    print("SUCCESS!")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

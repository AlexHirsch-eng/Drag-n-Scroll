"""
Final test script to verify the learning API works correctly
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

print("=" * 60)
print("TESTING LEARNING API ENDPOINTS")
print("=" * 60)

# Step 1: Login
print("\n[1] Testing login...")
login_response = requests.post(f"{BASE_URL}/auth/jwt/create/", json={
    "username": "testuser",
    "password": "testpass123"
})

if login_response.status_code == 200:
    token = login_response.json().get('access')
    print(f"   Login successful! Token: {token[:20]}...")
else:
    print(f"   Login failed: {login_response.status_code}")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

# Step 2: Test main-screen endpoint
print("\n[2] Testing /api/learning/main-screen/...")
main_screen_response = requests.get(f"{BASE_URL}/learning/main-screen/", headers=headers)

print(f"   Status: {main_screen_response.status_code}")

if main_screen_response.status_code == 200:
    data = main_screen_response.json()
    print(f"   Course Day: {data['current_course_day']['day_number']} - {data['current_course_day']['title']}")
    print(f"   Session A: {'Active' if data['session_a'] else 'None'}")
    print(f"   Session B: {'Active' if data['session_b'] else 'None'}")
    print(f"   XP Total: {data['xp_total']}")
    print(f"   Streak: {data['streak_days']} days")
    print("   SUCCESS!")
elif main_screen_response.status_code == 401:
    print("   ERROR: Unauthorized (401) - Token issue")
elif main_screen_response.status_code == 404:
    print("   ERROR: Not Found (404) - URL routing issue")
else:
    print(f"   ERROR: {main_screen_response.status_code}")
    print(f"   Details: {main_screen_response.text[:200]}")

# Step 3: Test courses endpoint
print("\n[3] Testing /api/course/...")
courses_response = requests.get(f"{BASE_URL}/course/", headers=headers)

if courses_response.status_code == 200:
    courses = courses_response.json()
    if isinstance(courses, list) and len(courses) > 0:
        print(f"   Found {len(courses)} courses")
        print(f"   First course: HSK {courses[0].get('hsk_level')} - {courses[0].get('title', 'N/A')}")
        print("   SUCCESS!")
    else:
        print(f"   Response: {str(courses)[:200]}")
else:
    print(f"   ERROR: {courses_response.status_code}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
print("\nFrontend URL: http://localhost:5173")
print("Backend URL:  http://localhost:8000")
print("\nIf tests passed, open the frontend in your browser!")

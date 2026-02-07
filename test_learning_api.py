"""
Test script to verify learning API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

# First, let's create/login a user
login_data = {
    "username": "testuser",
    "password": "testpass123"
}

# Try to login
print("1. Testing login...")
response = requests.post(f"{BASE_URL}/auth/jwt/create/", json=login_data)
print(f"Login status: {response.status_code}")

if response.status_code == 200:
    tokens = response.json()
    access_token = tokens.get('access')
    print(f"Got access token: {access_token[:20]}...")

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Test main-screen endpoint
    print("\n2. Testing /api/learning/main-screen/...")
    response = requests.get(f"{BASE_URL}/learning/main-screen/", headers=headers)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print("Success! Response data:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Error: {response.text}")

    # Test getting courses
    print("\n3. Testing /api/course/...")
    response = requests.get(f"{BASE_URL}/course/", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Courses endpoint works!")
    else:
        print(f"Error: {response.text}")

else:
    print(f"Login failed: {response.text}")
    print("\nTrying to register user...")

    # Try to register
    register_data = {
        "username": "testuser",
        "password": "testpass123",
        "email": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/auth/users/", json=register_data)
    print(f"Register status: {response.status_code}")
    if response.status_code == 201:
        print("User registered! Please run script again to test.")
    else:
        print(f"Register failed: {response.text}")

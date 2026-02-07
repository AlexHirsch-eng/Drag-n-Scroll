"""
Test API stability with multiple requests
"""
import requests
import time

BASE_URL = "http://localhost:8000/api"

# Login first
login_response = requests.post(f"{BASE_URL}/auth/jwt/create/", json={
    "username": "testuser",
    "password": "testpass123"
})
token = login_response.json().get('access')
headers = {"Authorization": f"Bearer {token}"}

print("Testing API stability with 20 consecutive requests...")
print("=" * 60)

success_count = 0
error_count = 0
errors = []

for i in range(20):
    try:
        response = requests.get(f"{BASE_URL}/learning/main-screen/", headers=headers)
        if response.status_code == 200:
            success_count += 1
            print(f"Request {i+1}: OK (200)")
        else:
            error_count += 1
            errors.append(f"Request {i+1}: Status {response.status_code}")
            print(f"Request {i+1}: ERROR ({response.status_code})")
    except Exception as e:
        error_count += 1
        errors.append(f"Request {i+1}: {str(e)}")
        print(f"Request {i+1}: EXCEPTION - {str(e)}")

    time.sleep(0.1)  # Small delay between requests

print("=" * 60)
print(f"Results: {success_count} successful, {error_count} errors")
if errors:
    print("\nErrors:")
    for error in errors:
        print(f"  {error}")

if error_count == 0:
    print("\n✓ API is stable! All requests succeeded.")
else:
    print(f"\n✗ API has {error_count} errors out of 20 requests")

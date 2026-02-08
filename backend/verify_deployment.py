#!/usr/bin/env python
"""
Deployment verification script for Drag'n'Scroll backend.
Run this after deploying to Render to verify everything is working.
"""

import os
import sys
import requests
from urllib.parse import urlparse

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.ENDC} {msg}")

def print_error(msg):
    print(f"{Colors.RED}✗{Colors.ENDC} {msg}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.ENDC} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.ENDC} {msg}")

def check_endpoint(url, expected_status=None, auth_header=None):
    """Check if an endpoint returns the expected status"""
    try:
        headers = {}
        if auth_header:
            headers['Authorization'] = auth_header

        response = requests.get(url, headers=headers, timeout=10)

        if expected_status:
            if response.status_code == expected_status:
                print_success(f"{url} → {response.status_code} (expected {expected_status})")
                return True, response
            else:
                print_error(f"{url} → {response.status_code} (expected {expected_status})")
                return False, response
        else:
            print_success(f"{url} → {response.status_code}")
            return True, response
    except requests.exceptions.Timeout:
        print_error(f"{url} → Request timeout")
        return False, None
    except requests.exceptions.ConnectionError:
        print_error(f"{url} → Connection error (service may not be running)")
        return False, None
    except Exception as e:
        print_error(f"{url} → {str(e)}")
        return False, None

def main():
    print(f"\n{Colors.BOLD}=== Drag'n'Scroll Backend Deployment Verification ==={Colors.ENDC}\n")

    # Get API base URL from environment or use default
    api_base = os.environ.get('API_BASE_URL', 'https://drag-n-scroll.onrender.com/api')

    print_info(f"Testing API at: {api_base}")
    print()

    # Test results
    results = {}

    # 1. Health check (should be 200)
    print(f"{Colors.BOLD}1. Health Check{Colors.ENDC}")
    success, response = check_endpoint(f"{api_base}/health/", 200)
    results['health'] = success
    if success:
        data = response.json()
        print_info(f"   Status: {data.get('status')}")
        print_info(f"   Database: {data.get('database')}")
    print()

    # 2. Main screen without auth (should be 401 Unauthorized)
    print(f"{Colors.BOLD}2. Main Screen (without auth){Colors.ENDC}")
    success, response = check_endpoint(f"{api_base}/learning/main-screen/", 401)
    results['main_screen_auth'] = success
    if not success and response and response.status_code == 404:
        print_error("   Endpoint returns 404 - URL routing may not be working!")
    print()

    # 3. Auth endpoints (should exist)
    print(f"{Colors.BOLD}3. Auth Endpoints{Colors.ENDC}")
    success, _ = check_endpoint(f"{api_base}/auth/users/", 401)
    results['auth_users'] = success
    success, _ = check_endpoint(f"{api_base}/auth/jwt/create/", 405)  # Method not allowed for GET
    results['auth_jwt'] = success
    print()

    # 4. Check CORS headers
    print(f"{Colors.BOLD}4. CORS Check{Colors.ENDC}")
    try:
        response = requests.options(f"{api_base}/health/", timeout=10)
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials'),
        }
        if cors_headers['Access-Control-Allow-Origin']:
            print_success(f"CORS Allowed Origin: {cors_headers['Access-Control-Allow-Origin']}")
            results['cors'] = True
        else:
            print_warning("No CORS headers found")
            results['cors'] = False
    except Exception as e:
        print_error(f"Failed to check CORS: {e}")
        results['cors'] = False
    print()

    # Summary
    print(f"{Colors.BOLD}=== Summary ==={Colors.ENDC}")
    total = len(results)
    passed = sum(results.values())
    failed = total - passed

    print(f"Total checks: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.ENDC}")
    print(f"{Colors.RED}Failed: {failed}{Colors.ENDC}")
    print()

    if failed == 0:
        print_success(f"{Colors.BOLD}{Colors.GREEN}All checks passed! Backend is deployed correctly.{Colors.ENDC}")
        return 0
    else:
        print_error(f"{Colors.BOLD}{Colors.RED}Some checks failed. Please review the errors above.{Colors.ENDC}")
        return 1

if __name__ == '__main__':
    sys.exit(main())

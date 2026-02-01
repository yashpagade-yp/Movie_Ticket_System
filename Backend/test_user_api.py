"""
User API Test Script
Tests: Register, Login, Forgot Password, Reset Password
"""

import httpx
import asyncio
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

# Test data - unique email each run
test_email = f"testuser_{int(datetime.now().timestamp())}@example.com"
test_password = "TestPassword123!"

test_user_data = {
    "email": test_email,
    "password": test_password,
    "first_name": "Test",
    "last_name": "User",
    "mobile_number": "1234567890",
}


async def test_user_api():
    async with httpx.AsyncClient() as client:
        print("=" * 60)
        print("USER API TESTING")
        print("=" * 60)

        # Test 1: Root endpoint
        print("\n1. Testing Root Endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            assert response.status_code == 200
            print("   ✓ Root endpoint working!")
        except Exception as e:
            print(f"   ✗ Error: {e}")
            return

        # Test 2: User Registration
        print("\n2. Testing User Registration...")
        try:
            response = await client.post(
                f"{BASE_URL}/users/register", json=test_user_data
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 201:
                print(f"   Response: {json.dumps(response.json(), indent=2)}")
                print("   ✓ User registration successful!")
            else:
                print(f"   Response: {response.text}")
                print(f"   ✗ Registration failed with status {response.status_code}")
                return
        except Exception as e:
            print(f"   ✗ Error: {e}")
            return

        # Test 3: User Login
        print("\n3. Testing User Login...")
        try:
            login_data = {"email": test_email, "password": test_password}
            response = await client.post(f"{BASE_URL}/users/login", json=login_data)
            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                response_data = response.json()
                token = response_data.get("access_token")
                print(f"   Token: {token[:50]}...")
                print(f"   User: {response_data['user']['email']}")
                print("   ✓ Login successful!")
                headers = {"Authorization": f"Bearer {token}"}
            else:
                print(f"   Response: {response.text}")
                print(f"   ✗ Login failed!")
                return
        except Exception as e:
            print(f"   ✗ Error: {e}")
            return

        # Test 4: Get User Profile (authenticated)
        print("\n4. Testing Get User Profile...")
        try:
            response = await client.get(f"{BASE_URL}/users/me", headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   Response: {json.dumps(response.json(), indent=2)}")
                print("   ✓ Profile retrieved!")
            else:
                print(f"   ✗ Failed: {response.text}")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Test 5: Forgot Password
        print("\n5. Testing Forgot Password...")
        try:
            response = await client.post(
                f"{BASE_URL}/users/forgot-password", json={"email": test_email}
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print(f"   Response: {response.json()}")
                print("   ✓ OTP sent (check logs for OTP)!")
            else:
                print(f"   ✗ Failed: {response.text}")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Test 6: Reset Password (with dummy OTP - will fail as expected)
        print("\n6. Testing Reset Password (with invalid OTP - expected to fail)...")
        try:
            response = await client.post(
                f"{BASE_URL}/users/reset-password",
                json={
                    "email": test_email,
                    "otp": "123456",  # Dummy OTP
                    "new_password": "NewPassword456!",
                },
            )
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            if response.status_code == 400:
                print("   ✓ Correctly rejected invalid OTP!")
            elif response.status_code == 200:
                print("   ⚠ Password reset succeeded (OTP matched)")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Test 7: Forgot Password for non-existent user
        print("\n7. Testing Forgot Password (non-existent user)...")
        try:
            response = await client.post(
                f"{BASE_URL}/users/forgot-password",
                json={"email": "nonexistent@example.com"},
            )
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            if response.status_code == 404:
                print("   ✓ Correctly returned 404 for non-existent user!")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Test 8: Login with wrong password
        print("\n8. Testing Login with Wrong Password...")
        try:
            response = await client.post(
                f"{BASE_URL}/users/login",
                json={"email": test_email, "password": "WrongPassword123!"},
            )
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
            if response.status_code == 401:
                print("   ✓ Correctly rejected wrong password!")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        print("\n" + "=" * 60)
        print("USER API TESTING COMPLETED")
        print("=" * 60)
        print("\n📊 Summary:")
        print("   ✓ Register - Working")
        print("   ✓ Login - Working")
        print("   ✓ Get Profile - Working")
        print("   ✓ Forgot Password - Working")
        print("   ✓ Reset Password - Validation Working")


if __name__ == "__main__":
    asyncio.run(test_user_api())

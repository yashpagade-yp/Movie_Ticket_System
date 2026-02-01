import httpx
import asyncio
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

# Test data
test_user_data = {
    "email": f"testuser_{datetime.now().timestamp()}@example.com",
    "password": "TestPassword123!",
    "username": f"testuser_{int(datetime.now().timestamp())}",
    "first_name": "Test",
    "last_name": "User",
    "mobile_number": "1234567890",
}

test_movie_data = {
    "title": "Test Movie",
    "description": "A test movie for API testing",
    "duration_minutes": 120,
    "language": "English",
    "genres": ["Action", "Thriller"],
    "release_date": datetime.now().isoformat(),
    "status": "NOW_SHOWING",
}

test_theater_data = {
    "name": "Test Theater",
    "location": "Test City",
    "address": "123 Test Street, Test City, Test State",
    "contact_number": "9876543210",
}


async def test_api():
    async with httpx.AsyncClient() as client:
        print("=" * 60)
        print("MOVIE TICKET SYSTEM API TESTING")
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

        # Test 2: User Registration
        print("\n2. Testing User Registration...")
        try:
            response = await client.post(
                f"{BASE_URL}/users/register", json=test_user_data
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200 or response.status_code == 201:
                print(f"   Response: {response.json()}")
                print("   ✓ User registration successful!")
            else:
                print(f"   Response Text: {response.text}")
                try:
                    print(f"   Response JSON: {response.json()}")
                except:
                    pass
                print(f"   ⚠ Registration returned status {response.status_code}")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Test 3: User Login
        print("\n3. Testing User Login...")
        try:
            login_data = {
                "email": test_user_data["email"],
                "password": test_user_data["password"],
            }
            response = await client.post(f"{BASE_URL}/users/login", json=login_data)
            print(f"   Status: {response.status_code}")
            response_data = response.json()
            print(f"   Response: {json.dumps(response_data, indent=2)}")

            if response.status_code == 200:
                token = response_data.get("access_token")
                if token:
                    print("   ✓ Login successful! Token received.")
                    # Store token for authenticated requests
                    headers = {"Authorization": f"Bearer {token}"}
                else:
                    print("   ⚠ Login successful but no token in response")
                    headers = {}
            else:
                print(f"   ⚠ Login returned status {response.status_code}")
                headers = {}
        except Exception as e:
            print(f"   ✗ Error: {e}")
            headers = {}

        # Test 4: Get User Profile (if authenticated)
        if headers:
            print("\n4. Testing Get User Profile...")
            try:
                response = await client.get(f"{BASE_URL}/users/me", headers=headers)
                print(f"   Status: {response.status_code}")
                print(f"   Response: {json.dumps(response.json(), indent=2)}")
                if response.status_code == 200:
                    print("   ✓ User profile retrieved!")
            except Exception as e:
                print(f"   ✗ Error: {e}")

        # Test 5: Create Movie (if authenticated)
        # Note: Skipping movie creation as it requires ADMIN role
        # We'll test with existing movies or create via direct DB access if needed
        movie_id = None
        print("\n5. Testing Create Movie...")
        print("   ⚠ Skipped - Requires ADMIN role (current user is CUSTOMER)")

        # Test 6: Get All Movies
        print("\n6. Testing Get All Movies...")
        try:
            response = await client.get(f"{BASE_URL}/movies/")
            print(f"   Status: {response.status_code}")
            movies = response.json()
            print(f"   Found {len(movies)} movie(s)")
            if movies:
                print(f"   First movie: {json.dumps(movies[0], indent=2)}")
            if response.status_code == 200:
                print("   ✓ Movies retrieved successfully!")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Test 7: Create Theater (if authenticated)
        if headers:
            print("\n7. Testing Create Theater...")
            try:
                response = await client.post(
                    f"{BASE_URL}/theaters/", json=test_theater_data, headers=headers
                )
                print(f"   Status: {response.status_code}")
                response_data = response.json()
                print(f"   Response: {json.dumps(response_data, indent=2)}")
                if response.status_code == 200 or response.status_code == 201:
                    theater_id = response_data.get("id")
                    print(f"   ✓ Theater created with ID: {theater_id}")
                else:
                    print(
                        f"   ⚠ Theater creation returned status {response.status_code}"
                    )
                    theater_id = None
            except Exception as e:
                print(f"   ✗ Error: {e}")
                theater_id = None

        # Test 8: Get All Theaters
        print("\n8. Testing Get All Theaters...")
        try:
            response = await client.get(f"{BASE_URL}/theaters/")
            print(f"   Status: {response.status_code}")
            theaters = response.json()
            print(f"   Found {len(theaters)} theater(s)")
            if theaters:
                print(f"   First theater: {json.dumps(theaters[0], indent=2)}")
            if response.status_code == 200:
                print("   ✓ Theaters retrieved successfully!")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        # Test 9: Create Showtime (if we have movie and theater)
        if headers and movie_id and theater_id:
            print("\n9. Testing Create Showtime...")
            try:
                showtime_data = {
                    "movie_id": movie_id,
                    "theater_id": theater_id,
                    "screen_id": "screen_1",  # Placeholder
                    "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
                    "end_time": (
                        datetime.now() + timedelta(days=1, hours=2)
                    ).isoformat(),
                    "base_price": 12.50,
                    "is_active": True,
                }
                response = await client.post(
                    f"{BASE_URL}/showtimes/", json=showtime_data, headers=headers
                )
                print(f"   Status: {response.status_code}")
                response_data = response.json()
                print(f"   Response: {json.dumps(response_data, indent=2)}")
                if response.status_code == 200 or response.status_code == 201:
                    showtime_id = response_data.get("id")
                    print(f"   ✓ Showtime created with ID: {showtime_id}")
                else:
                    print(
                        f"   ⚠ Showtime creation returned status {response.status_code}"
                    )
            except Exception as e:
                print(f"   ✗ Error: {e}")
        else:
            print("\n9. Testing Create Showtime...")
            print("   ⚠ Skipped - Requires both movie_id and theater_id")

        # Test 10: Get All Showtimes
        print("\n10. Testing Get All Showtimes...")
        try:
            response = await client.get(f"{BASE_URL}/showtimes/")
            print(f"   Status: {response.status_code}")
            showtimes = response.json()
            print(f"   Found {len(showtimes)} showtime(s)")
            if showtimes:
                print(f"   First showtime: {json.dumps(showtimes[0], indent=2)}")
            if response.status_code == 200:
                print("   ✓ Showtimes retrieved successfully!")
        except Exception as e:
            print(f"   ✗ Error: {e}")

        print("\n" + "=" * 60)
        print("API TESTING COMPLETED")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_api())

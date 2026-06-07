# test_api.py
# Simple test script to verify the API works

import json
from app import create_app

# Create the Flask app
app = create_app()

# Create a test client
client = app.test_client()

print("=" * 60)
print("Testing Barber Booking System API")
print("=" * 60)

# Test 1: Health check
print("\n1. Testing Health Check (GET /)")
response = client.get('/')
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.get_json(), indent=2)}")

# Test 2: Create first booking
print("\n2. Creating First Booking (POST /bookings)")
booking1_data = {
    "customer_name": "John Doe",
    "barber_name": "Mike",
    "date": "2026-06-10",
    "time": "14:30"
}
response = client.post('/bookings', json=booking1_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.get_json(), indent=2)}")

# Test 3: Create second booking
print("\n3. Creating Second Booking (POST /bookings)")
booking2_data = {
    "customer_name": "Jane Smith",
    "barber_name": "Sarah",
    "date": "2026-06-11",
    "time": "10:00"
}
response = client.post('/bookings', json=booking2_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.get_json(), indent=2)}")

# Test 4: Get all bookings
print("\n4. Retrieving All Bookings (GET /bookings)")
response = client.get('/bookings')
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.get_json(), indent=2)}")

# Test 5: Delete a booking
print("\n5. Deleting Booking with ID 1 (DELETE /bookings/1)")
response = client.delete('/bookings/1')
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.get_json(), indent=2)}")

# Test 6: Get all bookings after deletion
print("\n6. Retrieving All Bookings After Deletion (GET /bookings)")
response = client.get('/bookings')
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.get_json(), indent=2)}")

# Test 7: Try to delete non-existent booking
print("\n7. Attempting to Delete Non-Existent Booking (DELETE /bookings/999)")
response = client.delete('/bookings/999')
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.get_json(), indent=2)}")

# Test 8: Invalid request (missing fields)
print("\n8. Testing Invalid Request - Missing Fields (POST /bookings)")
invalid_data = {
    "customer_name": "Invalid"
}
response = client.post('/bookings', json=invalid_data)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.get_json(), indent=2)}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)

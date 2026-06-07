# DATA FLOW EXPLANATION
# How data flows through the 4-layer architecture

## Overview
The application uses a 4-layer architecture to maintain clean separation of concerns:

```
HTTP REQUEST/RESPONSE
        ↓
    ROUTES LAYER      ← Handles HTTP, parses JSON, validates format
        ↓
    SERVICES LAYER    ← Business logic, data validation, rules
        ↓
    DATA LAYER        ← CRUD operations on bookings_db
        ↓
    MODELS LAYER      ← Data structure definition
```

---

## Example 1: Creating a Booking (POST /bookings)

### REQUEST:
```
POST /bookings
Content-Type: application/json

{
  "customer_name": "Alice",
  "barber_name": "Bob",
  "date": "2026-06-15",
  "time": "10:00"
}
```

### LAYER 1: ROUTES (routes/booking_routes.py)
```
@booking_bp.route('', methods=['POST'])
def create_booking():
    # 1. Extract JSON from HTTP request
    data = request.get_json()
    # → { "customer_name": "Alice", "barber_name": "Bob", ... }
    
    # 2. Validate request format (required fields present)
    if not all(key in data for key in [...]):
        return error 400
    # → Data format is valid
    
    # 3. Call SERVICE LAYER
    booking = create_new_booking(
        customer_name=data['customer_name'],
        barber_name=data['barber_name'],
        date=data['date'],
        time=data['time']
    )
    # → Receives dict: { "id": 1, "customer_name": "Alice", ... }
    
    # 4. Return HTTP response
    return jsonify(booking), 201
```

### LAYER 2: SERVICES (services/booking_service.py)
```
def create_new_booking(customer_name, barber_name, date, time):
    # 1. Receive parameters from routes
    # → customer_name="Alice", barber_name="Bob", date="2026-06-15", time="10:00"
    
    # 2. Could add business logic here (validation, rules, etc.)
    # → Currently simple, but here's where you'd add:
    #    - Validate time format
    #    - Check for double bookings
    #    - Validate barber exists
    
    # 3. Call DATA LAYER
    booking = create_booking(customer_name, barber_name, date, time)
    # → Receives Booking object: Booking(id=1, customer_name="Alice", ...)
    
    # 4. Convert to dict (for JSON response)
    return booking.to_dict()
    # → Returns dict: { "id": 1, "customer_name": "Alice", ... }
```

### LAYER 3: DATA (data/memory_db.py)
```
bookings_db = []  # In-memory list
next_id = 1

def create_booking(customer_name, barber_name, date, time):
    # 1. Receive parameters from service
    # → customer_name="Alice", barber_name="Bob", date="2026-06-15", time="10:00"
    
    # 2. Instantiate MODEL (booking.py)
    booking = Booking(
        id=next_id,           # 1
        customer_name="Alice",
        barber_name="Bob",
        date="2026-06-15",
        time="10:00"
    )
    # → Receives Booking object from models.booking
    
    # 3. Store in memory
    bookings_db.append(booking)
    # → bookings_db now contains [Booking(id=1, ...)]
    
    # 4. Increment ID counter
    next_id = 2
    
    # 5. Return to service
    return booking
    # → Returns Booking object
```

### LAYER 4: MODELS (models/booking.py)
```
class Booking:
    def __init__(self, id, customer_name, barber_name, date, time):
        self.id = id
        self.customer_name = customer_name
        self.barber_name = barber_name
        self.date = date
        self.time = time
    
    def to_dict(self):
        # Convert to JSON-serializable dictionary
        return {
            'id': 1,
            'customer_name': 'Alice',
            'barber_name': 'Bob',
            'date': '2026-06-15',
            'time': '10:00'
        }
```

### RESPONSE:
```
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "id": 1,
  "customer_name": "Alice",
  "barber_name": "Bob",
  "date": "2026-06-15",
  "time": "10:00"
}
```

---

## Example 2: Getting All Bookings (GET /bookings)

### REQUEST:
```
GET /bookings
```

### DATA FLOW:
```
ROUTE LAYER:
  1. client.get('/bookings')
  2. Call fetch_all_bookings() → SERVICE
  
SERVICE LAYER:
  1. fetch_all_bookings()
  2. Call get_all_bookings() → DATA
  3. Convert each Booking to dict
  4. Return list of dicts
  
DATA LAYER:
  1. get_all_bookings()
  2. Return bookings_db (list of Booking objects)
  
RESPONSE:
  HTTP 200 OK with JSON array
```

---

## Example 3: Deleting a Booking (DELETE /bookings/1)

### REQUEST:
```
DELETE /bookings/1
```

### DATA FLOW:
```
ROUTE LAYER:
  1. Extract ID from URL path: booking_id=1
  2. Call remove_booking(1) → SERVICE
  3. Check if True or False
  4. Return 200 or 404
  
SERVICE LAYER:
  1. remove_booking(booking_id=1)
  2. Call delete_booking_by_id(1) → DATA
  3. Return True/False
  
DATA LAYER:
  1. delete_booking_by_id(booking_id=1)
  2. Find booking with id=1 in bookings_db
  3. Remove from list
  4. Return True if found, False if not found
```

---

## Why This Architecture?

### ✅ Separation of Concerns
- **Routes** don't know HOW to create bookings
- **Services** don't know HTTP details
- **Data** doesn't know business rules
- **Models** are just dumb data containers

### ✅ Testability
```python
# Can test service without Flask:
booking = create_new_booking("Alice", "Bob", "2026-06-15", "10:00")
assert booking['customer_name'] == "Alice"

# Can test data layer without service:
db.create_booking("Alice", "Bob", "2026-06-15", "10:00")
assert len(bookings_db) == 1
```

### ✅ Reusability
```python
# Same service can be called from different interfaces:
from services.booking_service import create_new_booking

# From Flask routes
@app.route('/bookings', methods=['POST'])
def create():
    booking = create_new_booking(...)

# From CLI
def cli():
    booking = create_new_booking(...)

# From scheduled task
def scheduled_task():
    booking = create_new_booking(...)
```

### ✅ Easy to Upgrade
```python
# Currently: memory_db.py uses list
bookings_db = []

# Future: Replace with database
from sqlalchemy import create_engine
engine = create_engine('postgresql://...')

# Services and routes don't change!
# They still call the same functions
```

### ✅ Maintainability
```python
# To understand what happens on POST /bookings:
# 1. Read routes/booking_routes.py (HTTP handling)
# 2. Read services/booking_service.py (logic)
# 3. Read data/memory_db.py (storage)
# Each layer is small and focused
```

---

## Summary: The Flow

Data flows IN from HTTP:
```
HTTP Request
    ↓
Routes (extract data, call service)
    ↓
Services (validate, process)
    ↓
Data (store/retrieve)
    ↓
Models (structure)
```

Data flows OUT to HTTP:
```
Models (structure data)
    ↓
Data (fetch from storage)
    ↓
Services (format for response)
    ↓
Routes (JSON-ify and return)
    ↓
HTTP Response
```

Each layer:
- **Takes input** from above
- **Does its job**
- **Passes output** to next layer
- **Has NO dependencies** on other layers (except the one below)

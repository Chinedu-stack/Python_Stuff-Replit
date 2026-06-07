# Barber Booking System - Flask Backend

A simple, modular Flask backend for a barber booking system demonstrating clean architecture and separation of concerns.

## Project Structure

```
├── app.py                      # Flask entry point
├── models/
│   ├── __init__.py
│   └── booking.py             # Booking data model
├── data/
│   ├── __init__.py
│   └── memory_db.py           # In-memory storage & helper functions
├── services/
│   ├── __init__.py
│   └── booking_service.py     # Business logic layer
├── routes/
│   ├── __init__.py
│   └── booking_routes.py      # Flask routes/endpoints
└── requirements.txt
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/` - Check if API is running
  ```json
  Response: { "status": "ok", "message": "..." }
  ```

### Create Booking
- **POST** `/bookings`
  ```json
  Request Body:
  {
    "customer_name": "John Doe",
    "barber_name": "Mike",
    "date": "2026-06-10",
    "time": "14:30"
  }
  
  Response (201 Created):
  {
    "id": 1,
    "customer_name": "John Doe",
    "barber_name": "Mike",
    "date": "2026-06-10",
    "time": "14:30"
  }
  ```

### Get All Bookings
- **GET** `/bookings`
  ```json
  Response (200 OK):
  [
    {
      "id": 1,
      "customer_name": "John Doe",
      "barber_name": "Mike",
      "date": "2026-06-10",
      "time": "14:30"
    }
  ]
  ```

### Delete Booking
- **DELETE** `/bookings/<id>`
  ```json
  Response (200 OK):
  { "message": "Booking deleted successfully" }
  
  Response (404 Not Found):
  { "error": "Booking not found" }
  ```

## Testing with curl

```bash
# Create a booking
curl -X POST http://localhost:5000/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Alice",
    "barber_name": "Bob",
    "date": "2026-06-15",
    "time": "10:00"
  }'

# Get all bookings
curl http://localhost:5000/bookings

# Delete a booking
curl -X DELETE http://localhost:5000/bookings/1
```

## Architecture Explanation: Data Flow

### The 4-Layer Architecture

#### 1. **Routes Layer** (routes/booking_routes.py)
- **Purpose**: Handle HTTP requests/responses
- **Responsibility**: Parse JSON, validate input format, call services
- **Important**: Contains NO business logic
- **Code**: Thin, mostly delegates to services

#### 2. **Services Layer** (services/booking_service.py)
- **Purpose**: Implement business logic
- **Responsibility**: Validate data, apply rules, coordinate data operations
- **Example**: Could add validation like "no double bookings same time"
- **Code**: Higher-level functions that call the data layer

#### 3. **Data Layer** (data/memory_db.py)
- **Purpose**: Manage data storage and retrieval
- **Responsibility**: Create, read, update, delete operations on bookings_db
- **Important**: Only knows about bookings_db list operations
- **Code**: Low-level helper functions (CRUD operations)

#### 4. **Models Layer** (models/booking.py)
- **Purpose**: Define data structure
- **Responsibility**: Represent booking data, provide to_dict() for JSON
- **Important**: No logic, just data
- **Code**: Simple class definition

### Example Request Flow: Creating a Booking

```
1. HTTP Request arrives at Flask route
   POST /bookings with JSON body
   
2. ROUTES LAYER (booking_routes.py)
   - extract JSON from request
   - validate fields are present
   - call service: create_new_booking(...)
   
3. SERVICES LAYER (booking_service.py)
   - receives parameters from route
   - could add business logic here (validation, rules)
   - calls data layer: create_booking(...)
   - converts Booking object to dict
   - returns dict
   
4. DATA LAYER (memory_db.py)
   - receives parameters from service
   - creates Booking object (uses models.Booking)
   - increments ID counter
   - appends to bookings_db list
   - returns Booking object
   
5. MODELS LAYER (booking.py)
   - Booking class instantiated in data layer
   - to_dict() called to convert for JSON
   
6. Response sent back
   - dict → JSON → HTTP 201 Created response
```

### Benefits of This Architecture

✅ **Separation of Concerns**: Each layer has one job
✅ **Testability**: Can test each layer independently
✅ **Maintainability**: Easy to understand and modify
✅ **Scalability**: Can add database to data layer without changing routes
✅ **Reusability**: Services can be called from different routes/interfaces

### Future Improvements

- Add data validation in services layer
- Replace memory_db with real database (PostgreSQL, MongoDB)
- Add business rules (no double bookings, hours validation)
- Add authentication/authorization
- Add logging
- Add unit tests

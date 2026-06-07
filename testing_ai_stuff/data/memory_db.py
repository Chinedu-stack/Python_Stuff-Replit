# data/memory_db.py
# In-memory storage for bookings and helper functions

from models.booking import Booking

# In-memory list to store all bookings
bookings_db = []

# Counter for generating unique IDs
next_id = 1


def create_booking(customer_name, barber_name, date, time):
    """
    Create a new booking and store it in memory.
    Returns the created Booking object.
    """
    global next_id
    
    # Create new booking with auto-incremented ID
    booking = Booking(
        id=next_id,
        customer_name=customer_name,
        barber_name=barber_name,
        date=date,
        time=time
    )
    
    # Add to in-memory database
    bookings_db.append(booking)
    
    # Increment ID for next booking
    next_id += 1
    
    return booking


def get_all_bookings():
    """
    Retrieve all bookings from memory.
    Returns a list of Booking objects.
    """
    return bookings_db


def get_booking_by_id(booking_id):
    """
    Find a booking by its ID.
    Returns the Booking object or None if not found.
    """
    for booking in bookings_db:
        if booking.id == booking_id:
            return booking
    return None


def delete_booking_by_id(booking_id):
    """
    Delete a booking by its ID.
    Returns True if deleted, False if booking not found.
    """
    global bookings_db
    
    # Find and remove the booking
    for i, booking in enumerate(bookings_db):
        if booking.id == booking_id:
            bookings_db.pop(i)
            return True
    
    return False

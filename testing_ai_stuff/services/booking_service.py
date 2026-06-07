# services/booking_service.py
# Business logic for booking operations

from data.memory_db import (
    create_booking,
    get_all_bookings,
    get_booking_by_id,
    delete_booking_by_id
)


def create_new_booking(customer_name, barber_name, date, time):
    """
    Business logic to create a booking.
    
    This layer can be extended to add validation, business rules, etc.
    Currently it delegates to the data layer.
    
    Args:
        customer_name (str): Name of the customer
        barber_name (str): Name of the barber
        date (str): Booking date (e.g., "2026-06-10")
        time (str): Booking time (e.g., "14:30")
    
    Returns:
        dict: Created booking as dictionary
    """
    booking = create_booking(customer_name, barber_name, date, time)
    return booking.to_dict()


def fetch_all_bookings():
    """
    Business logic to retrieve all bookings.
    
    Returns:
        list: All bookings as dictionaries
    """
    bookings = get_all_bookings()
    return [booking.to_dict() for booking in bookings]


def fetch_booking(booking_id):
    """
    Business logic to retrieve a specific booking.
    
    Args:
        booking_id (int): The ID of the booking
    
    Returns:
        dict: Booking as dictionary, or None if not found
    """
    booking = get_booking_by_id(booking_id)
    if booking:
        return booking.to_dict()
    return None


def remove_booking(booking_id):
    """
    Business logic to delete a booking.
    
    Args:
        booking_id (int): The ID of the booking to delete
    
    Returns:
        bool: True if deleted successfully, False if not found
    """
    return delete_booking_by_id(booking_id)

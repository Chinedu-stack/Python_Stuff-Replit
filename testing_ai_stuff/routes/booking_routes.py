# routes/booking_routes.py
# Flask routes for booking endpoints
# NOTE: Routes should be thin - all business logic goes to the service layer

from flask import Blueprint, request, jsonify
from services.booking_service import (
    create_new_booking,
    fetch_all_bookings,
    remove_booking
)

# Create a blueprint for booking routes
booking_bp = Blueprint('bookings', __name__, url_prefix='/bookings')


@booking_bp.route('', methods=['POST'])
def create_booking():
    """
    Create a new booking.
    
    Expected JSON body:
    {
        "customer_name": "John Doe",
        "barber_name": "Mike",
        "date": "2026-06-10",
        "time": "14:30"
    }
    
    Route layer responsibility:
    - Extract request data
    - Validate request format
    - Call service layer
    - Return appropriate HTTP response
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(key in data for key in 
            ['customer_name', 'barber_name', 'date', 'time']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Call service layer to handle business logic
        booking = create_new_booking(
            customer_name=data['customer_name'],
            barber_name=data['barber_name'],
            date=data['date'],
            time=data['time']
        )
        
        return jsonify(booking), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@booking_bp.route('', methods=['GET'])
def get_bookings():
    """
    Retrieve all bookings.
    
    Route layer responsibility:
    - Call service layer
    - Return list of bookings as JSON
    """
    try:
        bookings = fetch_all_bookings()
        return jsonify(bookings), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@booking_bp.route('/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    """
    Delete a booking by ID.
    
    Route layer responsibility:
    - Extract ID from URL
    - Call service layer to handle deletion
    - Return appropriate response
    """
    try:
        # Call service layer
        success = remove_booking(booking_id)
        
        if success:
            return jsonify({'message': 'Booking deleted successfully'}), 200
        else:
            return jsonify({'error': 'Booking not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

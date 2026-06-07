# models/booking.py
# Data class representing a booking

class Booking:
    """
    Represents a single barber booking.
    This is a simple data model with no business logic.
    """
    
    def __init__(self, id, customer_name, barber_name, date, time):
        self.id = id
        self.customer_name = customer_name
        self.barber_name = barber_name
        self.date = date
        self.time = time
    
    def to_dict(self):
        """Convert booking to dictionary for JSON response"""
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'barber_name': self.barber_name,
            'date': self.date,
            'time': self.time
        }

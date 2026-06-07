# app.py
# Flask application entry point
# This file initializes Flask and registers all routes

from flask import Flask, jsonify

# Import the booking routes blueprint
from routes.booking_routes import booking_bp


def create_app():
    """
    Flask application factory.
    Initializes the Flask app and registers blueprints.
    
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    # Register the booking routes blueprint
    # All routes defined in booking_bp will be prefixed with /bookings
    app.register_blueprint(booking_bp)
    
    # Root endpoint (health check)
    @app.route('/', methods=['GET'])
    def health_check():
        """Simple health check endpoint"""
        return jsonify({
            'status': 'ok',
            'message': 'Barber Booking System API is running'
        }), 200
    
    return app


if __name__ == '__main__':
    # Create and run the Flask app
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

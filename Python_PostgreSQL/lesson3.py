import psycopg
connection = psycopg.connect(
    dbname="barber_app",
    user="postgres",
    password="Legendx24j@",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()


def create_booking(customer_id, barber_id, booking_time):

    try:
        cursor.execute("""
INSERT INTO bookings (customer_id, barber_id, booking_time)
VALUES (%s, %s, %s)
RETURNING booking_id""",
(customer_id, barber_id, booking_time))

        booking_id = cursor.fetchone()[0]

        cursor.execute("""
UPDATE barbers
SET available = false
WHERE barber_id = %s
""",  
(barber_id,))

        connection.commit()
        print(f"Booking created successfully. Id: {booking_id}")
        return booking_id

    except Exception as error:
        print(f"There is an error here: {error}")
        connection.rollback()
        return None

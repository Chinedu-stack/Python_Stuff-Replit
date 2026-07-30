import psycopg

connection = psycopg.connect(
    dbname="barber_app",
    user="postgres",
    password="Legendx24j@",
    host="localhost",
    port="5432"
)

cursor = connection.cursor()

cursor.execute(
    """
    SELECT *
    FROM bookings
    WHERE id = 97;
    """
)

booking = cursor.fetchone()

print(booking)
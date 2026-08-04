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
    """DELETE FROM bookings
    WHERE booking_id = %s """,
    (45,)

)

connection.commit()
print("Success")
import psycopg


def get_connection():
    connection = psycopg.connect(
        dbname="barber_app",
        user="postgres",
        password="Legendx24j@",
        host="localhost",
        port="5432"
    )
    return connection



def execute_query(connection, query, parameters=None, fetch=False, update=False):
    cursor = connection.cursor()

    try:
        cursor.execute(query, parameters)
        if fetch != "one" and fetch != "all" and fetch != False:
            raise Exception(f"{fetch} is not a valid option for fetch")
        
        elif fetch and update:
            raise Exception("Fetch and update cannot both be True")
        
        elif fetch == "one":
            result = cursor.fetchone()[0]
            return result
 

        elif fetch == "all":
            result = cursor.fetchall()
            return result


        elif update:
            row_count = cursor.rowcount
            return row_count

        else:
            return None





        


    finally:
        cursor.close()

        

def create_booking(customer_id, barber_id, booking_time):
    connection = get_connection()

    try:
        booking_id = execute_query(connection, """
INSERT INTO bookings (customer_id, barber_id, booking_time)
VALUES (%s, %s, %s)
RETURNING booking_id""",
(customer_id, barber_id, booking_time), fetch="one")

    

        row_count = execute_query(connection, """
UPDATE barbers
SET available = false
WHERE barber_id = %s
AND available = true
""",  (barber_id,), update=True)

        if row_count == 0:
            raise Exception("Barber does not exist or is unavailable")

        

        print(f"Booking created successfully. Id: {booking_id}")
        connection.commit()
        return booking_id
        

    except Exception as error:
        print(f"There is an error here: {error}")
        connection.rollback()
        return None

    finally:
        connection.close()


connection = get_connection()
query = """
SELECT *
FROM bookings
WHERE booking_id = %s
"""
parameters = (67,)

result = execute_query(connection, query, parameters, fetch="Gih")
print(result)


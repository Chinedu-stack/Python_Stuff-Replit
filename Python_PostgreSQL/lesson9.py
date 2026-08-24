import psycopg

class InvalidQueryOptionsError(Exception):
    pass


class FetchUpdateConflictError(Exception):
    pass


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

    cursor = None

    try:
        cursor = connection.cursor()

        if fetch != "one" and fetch != "all" and fetch != False:
            raise InvalidQueryOptionsError(f"{fetch} is not a valid option for fetch")
            

        elif type(update) is not bool:
            raise InvalidQueryOptionsError("Update has an invalid value")
            
        
        elif fetch and update:
            raise FetchUpdateConflictError(f"Fetch and Update cannot both be true")


        cursor.execute(query, parameters)

        if fetch == "one":
            result = cursor.fetchone()[0]
            return result

        elif fetch == "all":
            result = cursor.fetchall()
            return result


        elif update is True:
            row_count = cursor.rowcount
            return row_count

        else:
            return None


    finally:
        if cursor is not None:
            cursor.close()      

def create_booking(customer_id, barber_id, booking_time):

    try:

        connection = get_connection()
        
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

def test():
    connection = get_connection()
    query = """
    SELECT *
    FROM bookings
    WHERE booking_id = %s
    """
    parameters = (68,)

    result = execute_query(connection, query, parameters, fetch="all")
    print(result)

test()
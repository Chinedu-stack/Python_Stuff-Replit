import psycopg
connection = psycopg.connect(
    dbname="barber_app",
    user="postgres",
    password="Legendx24j@",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()


def create_customer(name, phone_number):
    try:
        cursor.execute("""
        INSERT INTO customers(name, phone_number)
        VALUES(%s, %s)
        RETURNING customer_id
        """,
        (name, phone_number)
        )

        customer_id = cursor.fetchone()[0]

        connection.commit()

        return True, customer_id

    except Exception as error:
        connection.rollback()
        print(error)
        return False, None

    
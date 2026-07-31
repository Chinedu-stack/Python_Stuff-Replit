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
        INSERT INTO customers (name, phone_number)
        VALUES (%s, %s)
    """,
    ("Ahmed Mohammed", "07983412109")
)

connection.commit()
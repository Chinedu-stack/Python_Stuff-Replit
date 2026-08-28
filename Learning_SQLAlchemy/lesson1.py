from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import text

connection_url = URL.create(
    "postgresql+psycopg",
    username="postgres",
    password="Legendx24j@",
    host="localhost",
    port=5432,
    database="barber_app"
)

engine = create_engine(connection_url)

with engine.connect() as connection:
     result = connection.execute(
        text("SELECT * FROM barbers")
    )

     row = result.fetchone()

     print(row)
     print(row._mapping)
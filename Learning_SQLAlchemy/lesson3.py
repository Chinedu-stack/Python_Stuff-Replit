from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.engine import URL
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

connection_url = URL.create(
    "postgresql+psycopg",
    username="postgres",
    password="Legendx24j@",
    host="localhost",
    port=5432,
    database="barber_app"
)
engine = create_engine(connection_url)
session = Session(engine)


class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()


with engine.connect() as connection:

     
     result = connection.execute(
        text("""
            SELECT * FROM customers
            WHERE name = :name
        """),
         {"name": "Unique"}
        )
    

     row = result.fetchall()

     print(row)


statement = select(Customer)

result = session.execute(statement)
row = result.scalars()
for thing in row:
    print(thing.name)



# customers = result.scalars().all()
# print(customers)
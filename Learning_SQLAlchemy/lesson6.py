from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.engine import URL
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import or_

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

def get_customer_by_id(session, customer_id):
    statement = select(Customer).where(Customer.customer_id == customer_id)
    result = session.execute(statement)
    return result.scalars().one_or_none()

def get_customers_by_name(session, name):
    statement = select(Customer).where(Customer.name == name)
    result = session.execute(statement)
    customers = result.scalars().all()
    return customers

def get_customers_by_name_prefix(session, search):
    statement = ( select(Customer)
    .where(Customer.name.ilike(f"%{search}%"))
    .order_by(Customer.name)
    .limit(10)
    )
    result = session.execute(statement)
    customers = result.scalars().all()
    return customers

customers = get_customers_by_name_prefix(session, "A")
if customers:
    for customer in customers:
        print(customer.name)
from sqlalchemy import create_engine, select, ForeignKey
from sqlalchemy.orm import Session
from sqlalchemy.engine import URL
from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import or_
from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime

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
    bookings = relationship("Booking", back_populates="customer")

class Booking(Base):
    __tablename__ = "bookings"

    booking_id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.customer_id")
    )
    customer = relationship("Customer", back_populates="bookings")


    barber_id: Mapped[int] = mapped_column(
       ForeignKey("barbers.barber_id") 
    )

    barber = relationship("Barber", back_populates="bookings")

    booking_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    completed: Mapped[bool] = mapped_column()
    
    price: Mapped[Decimal] = mapped_column()


class Barber(Base):
    __tablename__ = "barbers"

    barber_id : Mapped[int] = mapped_column(Integer, primary_key = True)
    name: Mapped[str] = mapped_column(nullable=False)
    speciality: Mapped[str] = mapped_column()
    years_of_experience: Mapped[int] = mapped_column()
    available: Mapped[bool] = mapped_column()
    phone_number: Mapped[str] = mapped_column(nullable=False, unique=True)

    bookings: Mapped[list["Booking"]] = relationship(
        "Booking",
        back_populates="barber"
    )


    
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



# statement = (select(Booking)
# .where(
#     Booking.barber_id == 1,
#     Booking.completed == False
#     )
# .order_by(Booking.booking_time.asc())
# )
# result = session.execute(statement)
# bookings = result.scalars().all()

statement = (select(Booking).join(Barber)
             .where(Barber.speciality == "Afro Hair")
             .order_by(Booking.booking_time.asc()))
result = session.execute(statement)
bookings = result.scalars().all()

for booking in bookings:
    print(f"Booking id:{booking.booking_id}\nBooking Time: {booking.booking_time}")




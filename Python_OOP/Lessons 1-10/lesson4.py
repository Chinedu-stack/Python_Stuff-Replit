class BookingSystem:
    def __init__(self):
        self.appointments = []

    def book(self, appointment):
        self.appointments.append(appointment)

    def details(self):
        for booking in self.appointments:
            booking.details()


class Customer:
    def __init__(self, name):
        self.name = name


class Barber:
    def __init__(self, name):
        self.name = name


class Appointment:
    def __init__(self, customer, barber, time):
        self.customer = customer
        self.barber = barber
        self.time = time

    def details(self):
        print(
            f"Customer: {self.customer.name}\n "
            f"Barber: {self.barber.name}\n "
            f"Time: {self.time}\n"
            "________________________________________\n"
        )


customer1 = Customer("Nedu")
barber1 = Barber("Ryan")

appointment1 = Appointment(customer1, barber1, "10:00")
appointment2 = Appointment(customer1, barber1, "12:00")

system = BookingSystem()

system.book(appointment1)
system.book(appointment2)

system.details()


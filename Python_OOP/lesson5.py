class BookingSystem:
    def __init__(self):
        self.appointments = []

    def book(self, appointment):
        conflict = False
        for booking in self.appointments:
            if booking.barber == appointment.barber and booking.time == appointment.time:
                print("Can't do this booking. The barber already has a booking.")
                conflict = True

        if not conflict:
            self.appointments.append(appointment)
            print("This booking is suitable")



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

customer1 = Customer("Chinedu")
customer2 = Customer("Daniel")
barber1 = Barber("Rohan")
barber2 = Barber("Rohan") 


appointment4 = Appointment(customer2, barber1, "14:00")
appointment5 = Appointment(customer2, barber2, "14:00")
system = BookingSystem()

system.book(appointment4)
system.book(appointment5)
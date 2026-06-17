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
            f"Customer: {self.customer.name}, "
            f"Barber: {self.barber.name}, "
            f"Time: {self.time}"
        )


customer1 = Customer("Nedu")
barber1 = Barber("Ryan")

appointment1 = Appointment(customer1, barber1, "10:00")
appointment2 = Appointment(customer1, barber1, "12:00")

appointment1.details()
appointment2.details()
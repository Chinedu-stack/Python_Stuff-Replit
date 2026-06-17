class Customer:
    def show_details(self):
        print(self.name)
        print(self.phone)

class Barber:
    def show_details(self):
        print(self.name)
        print(self.speciality)


class Appointment:
    def show_details(self):
        print(self.booking)

customer1 = Customer()
customer2 = Customer()

barber1 = Barber()
appointment1 = Appointment()

# Customer 1
customer1.name = "Sarah"
customer1.phone = "01928383433"

# Customer 2
customer2.name = "Mike"
customer2.phone = "07777777777"

# Barber
barber1.name = "Dan"
barber1.speciality = "tapers"

appointment1.booking = "Chinedu has a haircut next Wednesday"

customer1.show_details()
barber1.show_details()
appointment1.show_details()
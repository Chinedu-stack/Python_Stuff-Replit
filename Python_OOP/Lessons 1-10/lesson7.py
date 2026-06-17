class BookingSystem:
    def __init__(self):
        self.appointments = []

    def book(self, appointment):
        conflict = False
        for booking in self.appointments:
            if booking.barber == appointment.barber and booking.time == appointment.time:
                print("Can't do this booking. The barber already has a booking.")
                conflict = True
                break

        if not conflict:
            self.appointments.append(appointment)
            print("This booking is suitable")

    def cancel(self, customer, time, barber):
        found = False
        for booking in self.appointments:
            if booking.customer == customer and  booking.time == time and booking.barber == barber:
                self.appointments.remove(booking)
                found = True
                break
        if not found:
            print("You tried to delete a booking that doesn't exist")

    def all_barber_cancel(self, barber):
        to_remove = []
        for booking in self.appointments:
            if booking.barber == barber:
                to_remove.append(booking)
        if to_remove:
            for booking in to_remove:
                self.appointments.remove(booking)


                
                

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
    
    def change_time(self, new_time):
        self.time = new_time

customer1 = Customer("Chinedu")
customer2 = Customer("Daniel")

barber1 = Barber("Rohan")
barber2 = Barber("Carl") 


appointment1 = Appointment(customer1, barber1, "14:00")
appointment2 = Appointment(customer2, barber2, "14:00")
app3 = Appointment(customer2, barber2, "17:00")
app4 = Appointment(customer2, barber2, "19:00")
system = BookingSystem()

system.book(appointment1)
system.book(appointment2)
system.book(app3)
system.book(app4)

system.all_barber_cancel(barber1)
system.all_barber_cancel(barber2)





system.details()
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



    def reschedule(self, appointment, new_time):
        for booking in self.appointments:

            if booking.barber == appointment.barber and booking.time == new_time:
                print("That time is already taken")
                return

        if appointment in self.appointments:
            appointment.time = new_time
            print("Booking rescheduled")

        else:
            print("No booking found")
                    
                

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
barber2 = Barber("Carl") 


appointment1 = Appointment(customer1, barber1, "14:00")
appointment2 = Appointment(customer2, barber2, "14:00")
system = BookingSystem()

system.book(appointment1)
system.book(appointment2)

system.reschedule(appointment1, "13:59")
system.reschedule(appointment2, "4:00")


system.details()
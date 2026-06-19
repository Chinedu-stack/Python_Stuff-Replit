class BookingSystem: 
    def __init__(self):
        self.appointments = []
        self.next_id = 1

    def book(self, appointment):
        conflict = False
        for booking in self.appointments:
            if booking.barber == appointment.barber and booking.time == appointment.time:
                print("Can't do this booking. The barber already has a booking.")
                conflict = True
                break

        if not conflict:
            appointment.booking_id = self.next_id
            self.next_id += 1
            self.appointments.append(appointment)
            print("Appointment Booked.")

    def cancel(self, booking_id):
        found = False
        for booking in self.appointments:
            if booking.booking_id == booking_id:
                self.appointments.remove(booking)
                print("Booking Cancelled")
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

    def check_available(self, appointment, new_time):
        for booking in self.appointments:
                if booking.barber == appointment.barber and booking.time == new_time:
                    return False
            
        return True


    def change_time(self, booking_id, new_time):

        for booking in self.appointments:
            if booking.booking_id == booking_id:

                if self.check_available(booking, new_time):
                    booking.change_time(new_time)
                    print("Success. Time Changed")
                else:
                    print("Can't book that. Barber Busy.")

                return
        print("Booking bot found")
        

    def details(self):
        for booking in self.appointments:
            booking.details()


class Customer:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return (
            self.name == other.name
        )


class Barber:
    def __init__(self, name):
        self.name = name
    def __eq__(self, other):
        return (
            self.name == other.name
        )


class Booking:
    def __init__(self, customer, barber, time, booking_id=None):
        self.booking_id = booking_id
        self.customer = customer
        self.barber = barber
        self.time = time

    def __str__(self):
        return f"{self.booking_id}:{self.customer.name} with {self.barber.name} at {self.time}"

    def __repr__(self):
        return f"Booking({self.booking_id}, {self.customer.name}, {self.barber.name}, {self.time})"

    def __eq__(self, other):
        return (
            self.customer == other.customer and
            self.barber == other.barber and
            self.time == other.time
        )
        
    def details(self):
        print(
            f"Customer: {self.customer.name}\n "
            f"Barber: {self.barber.name}\n "
            f"Time: {self.time}\n"
            "________________________________________\n"
        )
    
    def change_time(self, new_time):
        self.time = new_time




cus1 = Customer("Chinedu")
cus2 = Customer("Chinedu")
barb1 = Barber("Taiwo")
system = BookingSystem()

app1 = Booking(cus1, barb1, "13:00")
app2 = Booking(cus1, barb1, "13:01")


system.book(app1)
system.book(app2)


system.change_time(app1.booking_id, "13:01")
system.change_time(app1.booking_id, "1992:01")


system.details()
class BookingSystem: 
    def __init__(self):
        self.appointments = []
        self.next_id = 1

    def add_booking(self, appointment):
        appointment.booking_id = self.next_id
        self.next_id += 1
        self.appointments.append(appointment)

    def remove_booking(self, booking_id):
        for booking in self.appointments:
            if booking.booking_id == booking_id:
                self.appointments.remove(booking)
                return True
        return False

    def get_booking(self, booking_id):
        for booking in self.appointments:
            if booking.booking_id == booking_id:
                return booking
            
        return None
    
    def get_all_bookings(self):
        return self.appointments
    
    def cancel_all_for_barber(self, barber):
        to_remove = []
        for booking in self.appointments:
            if booking.barber == barber:
                to_remove.append(booking)
        if to_remove:
            for booking in to_remove:
                self.appointments.remove(booking)


class BookingService:
    def __init__(self, system):
        self.system = system
        
    def book(self, appointment):
        bookings = self.system.get_all_bookings()
        for booking in bookings:
            if booking.barber == appointment.barber and booking.time == appointment.time:
                print("Can't do this booking. The barber already has a booking.")
                return


        self.system.add_booking(appointment)
        print("Appointment Booked.")

    def cancel(self, booking_id):
        booking = self.system.get_booking(booking_id)

        if not booking:
            print("Can't cancel booking does not exist.")
            return

        self.system.remove_booking(booking_id)
        print("Cancelled")

    def check_available(self, barber, new_time):
        bookings = self.system.get_all_bookings()
        for booking in bookings:
                if booking.barber == barber and booking.time == new_time:
                    return False
            
        return True

    def change_time(self, booking_id, new_time):
        booking = self.system.get_booking(booking_id)
        if not booking:
            print("Booking not found")
            return
        
        if self.check_available(booking.barber, new_time):
            booking.change_time(new_time)
            print("Success. Time Changed")
        else:
            print("Can't book that. Barber Busy.")
            
        
    def details(self):
        bookings = self.system.get_all_bookings()
        for booking in bookings:
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


barber1 = Barber("Chinedu")
customer1 = Customer("MoreBlessinz")

system = BookingSystem()
service = BookingService(system)

appointment1 = Booking(customer1, barber1, "17:00")
service.book(appointment1)
service.cancel(appointment1.booking_id)

service.details()


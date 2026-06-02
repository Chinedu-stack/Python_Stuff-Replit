class Barber:
    def __init__(self,name):
        self.name = name
    
    def introduce(self):
        print(f"Hello my name is {self.name}")


class Customer:
    def __init__(self, name, haircut):
        self.name = name
        self.haircut = haircut
        self.barber = None

    def greet(self):
        print(f"Hello Barber my name is {self.name} and i want to get a fresh {self.haircut} today.")

    def change_haircut(self, new_haircut):
        self.haircut = new_haircut
        print(f"""{self.name} now has a new haircut
              he wants a fresh {self.haircut}.""")
        
    def name_change(self, new_name):
        self.name = new_name
        print(f"New Name: {self.name}")

    def book(self, barber):
        self.barber = barber
        print(f"{self.name} has a booking with {barber.name}")
        print(self.name, self.haircut, self.barber)





barber1 = Barber("Chinedu")
barber2 = Barber("Adan")

customer1 = Customer("Tristan", "low taper fade")

barber1.introduce()
barber2.introduce()
customer1.greet()
customer1.change_haircut("buzzcut")
customer1.name_change("Dequavius")
customer1.book(barber2)
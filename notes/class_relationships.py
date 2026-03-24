# Class Relationships Notes

#Parent Class
class Vehicle:
    def __init__(self, model, brand):
        self.brand = brand
        self.model = model
    def move(self):
        print("Move!")

class Car(Vehicle):
    pass

class Boat(Vehicle):
    def move(self):
        print("Sail!")

class Plane(Vehicle):
    def move(self):
        print("Fly!")

    
car = Car("Ford", "Mustang")
boat = Boat("Ibiza", "Touring 20")
plane = Plane("Boeing", "747")

print(car.brand)
print(car.model)
print(boat.brand)
print(boat.model)

car.move()
boat.move()
plane.move()

class Library:
    def __init__(self, name, catalog = []):
        self.name = name
        self.catalog = catalog
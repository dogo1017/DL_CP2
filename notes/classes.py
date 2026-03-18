#DL 1st, classes 

class Animal:
    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age

    def __str__(self):
        return f"Name: {self.name} \nSpecies: {self.species}\n Age: {self.age}"
    
    def birthday(self):
        self.age += 1

dog = Animal("Doug", "Dog", 4)
bunny = Animal("Judy", "Rabbit", 20)
print(dog)
print(bunny)
dog.birthday()
print(dog)
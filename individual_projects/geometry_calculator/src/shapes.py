import math

class Circle:
    def __init__(self, radius, name):
        self.name = name
        self.radius = radius
        self.diameter = radius*2
        
    def area(self):
        return math.pi*(self.radius**2)
    
    def circumference(self):
        return math.pi * self.diameter

class Triangle:
    def __init__(self,name,sides):
        self.sides = sides
        self.name = name
    
    def perimeter(self):
            return self.sides[1]+self.sides[2]+self.sides[3] 
    
    def area(self):
        s = (self.sides[1]+self.sides[2]+self.sides[3])/2
        a = self.sides[1]
        b = self.sides[2]
        c = self.sides[3]
        return math.sqrt(s(s-a)(s-b)(s-c))
    
class Rectangle:
    def __init__(self,base,height,name):
        self.name = name
        self.base = base
        self.height = height

    def area(self):
        return self.base*self.height
    
    def perimeter(self):
        return (2*self.base) + (2*self.height)

class Square:
    def __init__(self,side,name):
        self.side = side
        self.name = name

    def area(self):
        return self.side*self.side

    def perimeter(self):
            return (4*self.side)
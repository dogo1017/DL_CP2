import math


class Circle:
    def __init__(self, radius, name):
        self.name = name
        self.radius = float(radius)
        self.diameter = self.radius * 2

    def area(self):
        return round(math.pi * (self.radius ** 2), 2)

    def perimeter(self):
        return round(math.pi * self.diameter, 2)

    def info(self):
        return f"Circle | {self.name} | r={self.radius}"

    def display(self):
        print("📊 CIRCLE DETAILS:")
        print("┌─────────────────────────────────────┐")
        print(f"│ Shape:     Circle #{self.name:<19}│")
        print(f"│ Radius:    {str(self.radius) + ' units':<26}│")
        print(f"│ Area:      {str(self.area()) + ' units²':<26}│")
        print(f"│ Perimeter: {str(self.perimeter()) + ' units':<26}│")
        print(f"│ Diameter:  {str(self.diameter) + ' units':<26}│")
        print("└─────────────────────────────────────┘")

    def formula(self):
        print("  Circle:")
        print("    Area      = pi x r squared")
        print("    Perimeter = pi x diameter")


class Rectangle:
    def __init__(self, base, height, name):
        self.name = name
        self.base = float(base)
        self.height = float(height)

    def area(self):
        return round(self.base * self.height, 2)

    def perimeter(self):
        return round((2 * self.base) + (2 * self.height), 2)

    def info(self):
        return f"Rectangle | {self.name} | b={self.base} h={self.height}"

    def display(self):
        print("📊 RECTANGLE DETAILS:")
        print("┌─────────────────────────────────────┐")
        print(f"│ Shape:     Rectangle #{self.name:<16}│")
        print(f"│ Base:      {str(self.base) + ' units':<26}│")
        print(f"│ Height:    {str(self.height) + ' units':<26}│")
        print(f"│ Area:      {str(self.area()) + ' units²':<26}│")
        print(f"│ Perimeter: {str(self.perimeter()) + ' units':<26}│")
        print("└─────────────────────────────────────┘")

    def formula(self):
        print("  Rectangle:")
        print("    Area      = base x height")
        print("    Perimeter = 2 x base + 2 x height")


class Square:
    def __init__(self, side, name):
        self.name = name
        self.side = float(side)

    def area(self):
        return round(self.side * self.side, 2)

    def perimeter(self):
        return round(4 * self.side, 2)

    def info(self):
        return f"Square | {self.name} | s={self.side}"

    def display(self):
        print("📊 SQUARE DETAILS:")
        print("┌─────────────────────────────────────┐")
        print(f"│ Shape:     Square #{self.name:<19}│")
        print(f"│ Side:      {str(self.side) + ' units':<26}│")
        print(f"│ Area:      {str(self.area()) + ' units²':<26}│")
        print(f"│ Perimeter: {str(self.perimeter()) + ' units':<26}│")
        print("└─────────────────────────────────────┘")

    def formula(self):
        print("  Square:")
        print("    Area      = side squared")
        print("    Perimeter = 4 x side")


class Triangle:
    def __init__(self, side1, side2, side3, name):
        self.name = name
        self.side1 = float(side1)
        self.side2 = float(side2)
        self.side3 = float(side3)

    def is_valid(self):
        a, b, c = self.side1, self.side2, self.side3
        return a + b > c and a + c > b and b + c > a

    def perimeter(self):
        return round(self.side1 + self.side2 + self.side3, 2)

    def area(self):
        s = (self.side1 + self.side2 + self.side3) / 2
        return round(math.sqrt(s * (s - self.side1) * (s - self.side2) * (s - self.side3)), 2)

    def info(self):
        return f"Triangle | {self.name} | s1={self.side1} s2={self.side2} s3={self.side3}"

    def display(self):
        print("📊 TRIANGLE DETAILS:")
        print("┌─────────────────────────────────────┐")
        print(f"│ Shape:     Triangle #{self.name:<17}│")
        print(f"│ Side 1:    {str(self.side1) + ' units':<26}│")
        print(f"│ Side 2:    {str(self.side2) + ' units':<26}│")
        print(f"│ Side 3:    {str(self.side3) + ' units':<26}│")
        print(f"│ Area:      {str(self.area()) + ' units²':<26}│")
        print(f"│ Perimeter: {str(self.perimeter()) + ' units':<26}│")
        print("└─────────────────────────────────────┘")

    def formula(self):
        print("  Triangle:")
        print("    Perimeter = s1 + s2 + s3")
        print("    Area      = sqrt(s(s-a)(s-b)(s-c))  [Heron's formula]")
        print("                where s = perimeter / 2")
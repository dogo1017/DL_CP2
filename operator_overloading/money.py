"""
Complete Lab 5 and update the following information:

Author: Douglas London
Date: 5/18
"""
class Money:
    def __init__(self, dollars, cents):
        self.dollars = dollars
        self.cents = cents
        self.normalize()

    def normalize(self):
        # carry over any cents >= 100 into dollars
        if self.cents >= 100:
            self.dollars += self.cents // 100
            self.cents = self.cents % 100

    def __str__(self):
        return f"${self.dollars}.{self.cents:02d}"


    # Part 1: overload + so two Money objects can be added
    def __add__(self, other):
        total_cents = (self.dollars * 100 + self.cents) + (other.dollars * 100 + other.cents)
        return Money(0, total_cents)


    # Part 2: overload * so Money can be multiplied by an integer
    def __mul__(self, scalar):
        total_cents = (self.dollars * 100 + self.cents) * scalar
        return Money(0, total_cents)

    # handle reversed case: 3 * m2
    def __rmul__(self, scalar):
        return self.__mul__(scalar)


    # Part 3: overload == so two Money objects are equal if dollars and cents match
    def __eq__(self, other):
        return self.dollars == other.dollars and self.cents == other.cents


def main():
    m1 = Money(3, 50)
    m2 = Money(2, 75)

    print("m1:", m1)
    print("m2:", m2)

    # Part 1: addition
    m3 = m1 + m2
    print("m3:", m3)

    # Part 2: multiplication both directions
    m4 = m1 * 2
    m5 = 3 * m2
    print("m4:", m4)
    print("m5:", m5)

    # Part 3: equality
    print(m1 == Money(2, 150))
    print(m1 == Money(3, 49))


if __name__ == "__main__":
    main()
# base class for all dessert items
class DessertItem:
    def __init__(self, name=""):
        self.name = name


# candy sold by the pound
class Candy(DessertItem):
    def __init__(self, name="", candy_weight=0.0, price_per_pound=0.0):
        super().__init__(name)
        self.candy_weight = candy_weight
        self.price_per_pound = price_per_pound


# cookies sold by the dozen
class Cookie(DessertItem):
    def __init__(self, name="", cookie_quantity=0, price_per_dozen=0.0):
        super().__init__(name)
        self.cookie_quantity = cookie_quantity
        self.price_per_dozen = price_per_dozen


# ice cream sold by the scoop
class IceCream(DessertItem):
    def __init__(self, name="", scoop_count=0, price_per_scoop=0.0):
        super().__init__(name)
        self.scoop_count = scoop_count
        self.price_per_scoop = price_per_scoop


# sundae extends IceCream with a topping
class Sundae(IceCream):
    def __init__(self, name="", scoop_count=0, price_per_scoop=0.0, topping_name="", topping_price=0.0):
        super().__init__(name, scoop_count, price_per_scoop)
        self.topping_name = topping_name
        self.topping_price = topping_price
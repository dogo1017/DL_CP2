# Defines the Account class with default values if not provided, then format object into readable string when printed
class Account:
    def __init__(self, owner: str = "", balance: float = 0.0):
        self.owner = owner
        self.balance = balance
    def __str__(self):
        return f"Owner: {self.owner}, Balance: ${self.balance:.2f}"
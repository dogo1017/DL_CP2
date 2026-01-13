#DL 1st, financial calculator

import os
import math

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


calcs = ["goal save", "compound interest", "budget allocator", "sales price", "tip calculator"]

# define stupid proofing function that takes in arguments of the required input, and datatype, and then using try and except to test if it is the right type


def sp_input(type):
    while True:
        user_input = input()
        try:
            if type == int:
                return int(user_input)
            if type == float:
                return float(user_input)
            if type == str:
                return str(user_input).strip().lower()
        except ValueError:
            print("That is not a valid input\n")
            continue


def back_to_menu():
    print("\n1) Back to menu\n2) Exit")
    choice = 0
    while choice != 1 and choice != 2:
        choice = sp_input(int)
        if choice != 1 and choice != 2:
            print("That is not a valid input")
    if choice == 1:
        clear_terminal()
        starting_menu(calcs)
    else:
        exit()


# goal_save function, uses stupid proof function to take in what they are saving to, how often they are contibuting (weekly/monthly), how much you contribute each time, then define gs_calc func that divides the total amount by the amount you contribute, and then printing off the amount of weeks/months it will take
def goal_save():
    print("Enter save goal:")
    save_goal = 0
    while save_goal <= 0:
        save_goal = sp_input(float)
        if save_goal <= 0:
            print("That is not a valid input")

    print("1) Monthly\n2) Weekly")
    contribute_time = 0
    while contribute_time != 1 and contribute_time != 2:
        contribute_time = sp_input(int)
        if contribute_time != 1 and contribute_time != 2:
            print("That is not a valid input")

    print("Enter contribution amount:")
    contribute_amount = 0
    while contribute_amount <= 0:
        contribute_amount = sp_input(float)
        if contribute_amount <= 0:
            print("That is not a valid input")

    clear_terminal()

    def gs_calc():
        save_time = save_goal / contribute_amount
        save_time = math.ceil(save_time)
        if contribute_time == 1:
            return f"{save_time} months"
        else:
            return f"{save_time} weeks"

    if contribute_time == 1:
        contribute_time = "Monthly"
    else:
        contribute_time = "Weekly"

    print(f"Contribution Type: {contribute_time}")
    print(f"Contribution Amount: ${round(contribute_amount,2)}")
    print(f"Save Goal: ${round(save_goal,2)}")
    print(f"Time Needed To Reach Goal: {gs_calc()}")
    back_to_menu()


# define compound_interest function that uses sp func to take in the starting amount, interest rate, years soent compounding, and then define the function ci_calc which takes the starting amount, multiplies the amount by the percent, adds it, and then loops through that process for as many years spent compounding
def compound_interest():
    print("Enter starting amount:")
    start_amount = sp_input(float)

    print("Enter interest rate (percent):")
    interest = sp_input(float) / 100

    print("Enter years compounding:")
    years = sp_input(int)

    def ci_calc():
        total = start_amount
        for i in range(years):
            total += total * interest
        return round(total, 2)

    clear_terminal()
    print(f"Starting Amount: ${round(start_amount,2)}")
    print(f"Interest Rate: {round(interest * 100,2)}%")
    print(f"Years: {years}")
    print(f"Final Amount: ${ci_calc()}")
    back_to_menu()


# define budget_allocator function that uses sp to take in how many categories, and for each category it asks for what it is called (saving the cateories to a list), then asks for monthy income, then for each category it will ask what percent their category is, then make a function ba_calc which loops for amount of categories and multiplies the percentage by the income, and prints it out
def budget_allocator():
    print("How many categories?")
    categories = []
    percents = []

    count = sp_input(int)

    for i in range(count):
        print("Enter category name:")
        categories.append(sp_input(str))

    print("Enter monthly income:")
    income = sp_input(float)

    for i in categories:
        print(f"Enter percent for {i}:")
        percents.append(sp_input(float) / 100)

    def ba_calc():
        for i in range(len(categories)):
            print(f"{categories[i]}: ${round(income * percents[i],2)}")

    clear_terminal()
    ba_calc()
    back_to_menu()


# define sales_price function that uses sp to take in the origonal cost of the item, the precent of discount, and orunts out the origonal cost - the percentage.
def sales_price():
    print("Enter original price:")
    price = sp_input(float)

    print("Enter discount percent:")
    discount = sp_input(float) / 100

    clear_terminal()
    print(f"Final Price: ${round(price - (price * discount),2)}")
    back_to_menu()


# define tip_calc that uses sp to take in how much the bill is, the precent of tip, and prints out the amount for tip and total after
def tip_calc():
    print("Enter bill amount:")
    bill = sp_input(float)

    print("Enter tip percent:")
    tip = sp_input(float) / 100

    clear_terminal()
    print(f"Tip Amount: ${round(bill * tip,2)}")
    print(f"Total: ${round(bill + (bill * tip),2)}")
    back_to_menu()


# define function starting_menu(Main function) that will give the user a menu with options to open the different calculator function
def starting_menu(calcs):
    print("FINANCIAL CALCULATOR")
    counter = 0
    for i in calcs:
        counter += 1
        print(f"{counter}) {i}")

    calc_choice = 0
    while calc_choice <= 0 or calc_choice > counter:
        print(f"Which calculator would you like to use(1-{counter}):")
        calc_choice = sp_input(int)
        if calc_choice <= 0 or calc_choice > counter:
            print("That is not a valid input")

    if calc_choice == 1:
        goal_save()
    elif calc_choice == 2:
        compound_interest()
    elif calc_choice == 3:
        budget_allocator()
    elif calc_choice == 4:
        sales_price()
    elif calc_choice == 5:
        tip_calc()


starting_menu(calcs)

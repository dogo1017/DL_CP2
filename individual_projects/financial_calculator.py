#DL 1st, financial calculator

import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


calcs = ["goal save"]

# define stupid proofing function that takes in arguments of the required input, and datatype, and then using try and except to test if it is the right type


def sp_input(type):
    while True:
        user_input = input()
        if type == 'int':
            try:
                return(int(user_input))
            except TypeError:
                print("That is not a valid input\n")
                continue
        if type == 'float':
            try:
                return(float(user_input))
            except TypeError:
                print("That is not a valid input\n")
                continue
        if type == 'str':
            try:
                return(str(user_input).strip().lower())
            except TypeError:
                print("That is not a valid input\n")
                continue
        
    


# goal_save function, uses stupid proof function to take in what they are saving to, how often they are contibuting (weekly/monthly), how much you contribute each time, then define gs_calc func that divides the total amount by the amount you contribute, and then printing off the amount of weeks/months it will take
def goal_save():
    print("1) Monthly\n2) Weekly")
    contribute_time = 0
    contribute_amount = 0
    save_goal = 0
    while save_goal <= 0:
        save_goal = sp_input(int)
        if save_goal <= 0:
            print("That is not a valid input")
    while contribute_time != 1 or contribute_time != 2:
        contribute_time = sp_input(int)
        if contribute_time != 1 or contribute_time != 2:
            print("That is not a valid input")
    while contribute_amount <= 0:
        contribute_amount = sp_input(int)
        if contribute_time <= 0:
            print("That is not a valid input")
    clear_terminal()
    def gs_calc():
            save_time = save_goal/contribute_amount
            if contribute_time == 1:
                save_time = f"{save_time} Months"
            else:
                save_time = f"{save_time} Weeks"
    if contribute_time == 1:
        contribute_time = "Monthly"
    else:
        contribute_time = "Weekly"
    print(f"Contribution Type: {contribute_time}")
    print(f"Contribution Amount: {contribute_amount}")
    print(f"Save Goal")
        

# define compound_interest function that uses sp func to take in the starting amount, interest rate, years soent compounding, and then define the function ci_calc which takes the starting amount, multiplies the amount by the percent, adds it, and then loops through that process for as many years spent compounding

# define budget_allocator function that uses sp to take in how many categories, and for each category it asks for what it is called (saving the cateories to a list), then asks for monthy income, then for each category it will ask what percent their category is, then make a function ba_calc which loops for amount of categories and multiplies the percentage by the income, and prints it out

# define sales_price function that uses sp to take in the origonal cost of the item, the precent of discount, and orunts out the origonal cost - the percentage.

# define tip_calc that uses sp to take in how much the bill is, the precent of tip, and prints out the amount for tip and total after

# define function starting_menu that will give the user a menu with options to open the different calculator function


def starting_menu(calcs):
    print("FINANCIAL CALCULATOR")
    counter = 0
    for i in calcs:
        counter += 1
        print(f"{counter}) {i}")
    calc_choice = 0
    while calc_choice <= 0 or calc_choice > counter: 
        print(f"Which calculator would you like to use(1-{counter}):")
        calc_choice = sp_input(str)
        print("That is not a valid input")
    if calc_choice == 1:
        goal_save()
    elif calc_choice == 2:
        compund_interest()
    elif calc_choice == 3:
        budget_allocator()
    elif calc_choice == 4:
        sales_prince()
    elif calc_choice == 5:
        tip_calc()
    else:
        print("That is not a valid input")


starting_menu(calcs)
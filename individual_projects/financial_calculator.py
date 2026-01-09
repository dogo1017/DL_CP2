#DL 1st, financial calculator

# define stupid proofing function that takes in arguments of the required input, and datatype, and then using try and except to test if it is the right type

def sp_input(type):
    user_input = input()
    if type == 'int':
        try:
            return(int(user_input))
        except:
            TypeError
    if type == 'float':
        try:
            return(float(user_input))
        except:
            TypeError
    if type == 'str':
        try:
            return(str(user_input))
        except:
            TypeError
    

# define function starting_menu that will give the user a menu with options to open the different calculator functions

def starting_menu(calcs):
    counter = 0
    for i in calcs:
        counter += 1
        print()

# goal_save function, uses stupid proof function to take in what they are saving to, how often they are contibuting (weekly/monthly), how much you contribute each time, then define gs_calc func that divides the total amount by the amount you contribute, and then printing off the amount of weeks/months it will take

# define compound_interest function that uses sp func to take in the starting amount, interest rate, years soent compounding, and then define the function ci_calc which takes the starting amount, multiplies the amount by the percent, adds it, and then loops through that process for as many years spent compounding

# define budget_allocator function that uses sp to take in how many categories, and for each category it asks for what it is called (saving the cateories to a list), then asks for monthy income, then for each category it will ask what percent their category is, then make a function ba_calc which loops for amount of categories and multiplies the percentage by the income, and prints it out

# define sales_price function that uses sp to take in the origonal cost of the item, the precent of discount, and orunts out the origonal cost - the percentage.

# define tip_calc that uses sp to take in how much the bill is, the precent of tip, and prints out the amount for tip and total after
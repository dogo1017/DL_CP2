import os
import shapes
def create_shape():
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def create_circle():
        while True:
            print("Creating a Circle...")
            user_input = input("Enter radius (positive number) or 'r' to return: ")
            if user_input == 'r':
                return
            if user_input < 0 or is_float(user_input) != True:
                os.system("cls")
                print(f"'{user_input}' is not a valid input")
                continue
            else:
                break
            
    def create_rectangle():
        length = 0
        height = 0
        while True:
            print("Creating a Rectangle...")
            user_input = input("Enter Length (positive number) or 'r' to return: ")
            if user_input == 'r':
                return
            if user_input < 0 or is_float(user_input) != True:
                os.system("cls")
                print(f"'{user_input}' is not a valid input")
                continue
            else:
                length = user_input
                break
        while True:
            print("Creating a Rectangle...")
            user_input = input("Enter height (positive number) or 'r' to return: ")
            if user_input == 'r':
                return
            if user_input < 0 or is_float(user_input) != True:
                os.system("cls")
                print(f"'{user_input}' is not a valid input")
                continue
            else:
                height = user_input
                break
        name = shapes.Rectangle(length,height)
        return name
    
    def create_square():
        while True:
            print("Creating a Square...")
            user_input = input("Enter side length (positive number) or 'r' to return: ")
            if user_input == 'r':
                return
            if user_input < 0 or is_float(user_input) != True:
                os.system("cls")
                print(f"'{user_input}' is not a valid input")
                continue
            else:
                height = user_input
                break
        name = shapes.Rectangle(height)
        return name

    def create_triangle():
        while True:
            print("Creating a Triangle...")
            user_input = input("Enter side1 length (positive number) or 'r' to return: ")
            if user_input == 'r':
                return
            if user_input < 0 or is_float(user_input) != True:
                os.system("cls")
                print(f"'{user_input}' is not a valid input")
                continue
            else:
                side1 = user_input
                break
        while True:
            print("Creating a Triangle...")
            user_input = input("Enter side2 length (positive number) or 'r' to return: ")
            if user_input == 'r':
                return
            if user_input < 0 or is_float(user_input) != True:
                os.system("cls")
                print(f"'{user_input}' is not a valid input")
                continue
            else:
                side2 = user_input
                break
        while True:
            print("Creating a Triangle...")
            user_input = input("Enter side3 length (positive number) or 'r' to return: ")
            if user_input == 'r':
                return
            if user_input < 0 or is_float(user_input) != True:
                os.system("cls")
                print(f"'{user_input}' is not a valid input")
                continue
            else:
                side3 = user_input
                break
        name = shapes.Rectangle(side1,side2,side3)
        return name

    name = input("Name Your shape or type 'r' to return")
    if name.strip().lower() == 'r':
        return 
    

    chosen_shape = input("[1] Circle⭕\n","[2] Rectangle📋","[3] Square⬜","[4] Triangle🔺","[5] Return")
    if chosen_shape == 1:
        create_circle()
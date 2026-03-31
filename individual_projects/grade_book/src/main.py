#DL main.py

import os
from gradebook import GradeBook
from menu import menu_add_student, menu_add_grade, menu_view_student, menu_view_all, menu_class_summary
from utils import print_header


# Builds the path to the CSV file relative to this file's location
def get_csv_path():
    src_dir = os.path.dirname(__file__)
    return os.path.join(src_dir, "..", "docs", "grades.csv")


# Clears the terminal and prints the main menu header and options
def show_main_menu():
    print_header("SIMPLE GRADE BOOK")
    print("  Welcome to the Class Grade Book!")
    print("\n  MAIN MENU:")
    print("  [1] Add New Student")
    print("  [2] Add Grade to Student")
    print("  [3] View Student Record")
    print("  [4] View All Students")
    print("  [5] Class Summary")
    print("  [6] Exit")


# Entry point - loads the gradebook from CSV then runs the menu loop until the user exits
def main():
    csv_path = get_csv_path()
    gradebook = GradeBook(csv_path)
    gradebook.load_from_csv()

    while True:
        show_main_menu()
        choice = input("\n  Enter your choice (1-6): ").strip()

        if choice == "1":
            menu_add_student(gradebook)
        elif choice == "2":
            menu_add_grade(gradebook)
        elif choice == "3":
            menu_view_student(gradebook)
        elif choice == "4":
            menu_view_all(gradebook)
        elif choice == "5":
            menu_class_summary(gradebook)
        elif choice == "6":
            print_header("GOODBYE")
            print("  See you next time!\n")
            break
        else:
            print("\n  Invalid choice. Please enter a number from 1 to 6.")
            input("  Press Enter to continue...")


main()
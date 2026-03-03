# DL 1st, personal library project

# Create a list that will store all books in the library, each book is stored as a tuple containing a title and an author
books = []

# Create a set that will store all author names, this is mainly included to meet the rubric requirement of using a set, set automatically prevents duplicate authors and is updated whenever a new book is added
authors_set = set()

# Define a function that safely gets user input, it runs inside a while loop so the user is repeatedly asked until valid input is entered, use try and except to prevent the program from crashing if the wrong data type is entered, and if use_set is True the input must match one of the allowed answers provided
def sp_input(use_set, answers, return_type):
    while True:
        user_input = input("> ")

        try:
            if return_type == int:
                user_input = int(user_input)
            elif return_type == float:
                user_input = float(user_input)
            elif return_type == str:
                user_input = user_input.strip()
        except ValueError:
            print("Invalid input, try again.")
            continue

        if use_set == True:
            if user_input in answers:
                return user_input
            else:
                print("That is not a valid option.")
        else:
            return user_input

# Define a function that displays all books currently stored in the library, it first checks if the list is empty, then uses a for loop to go through each book in the list and prints the title and author in a readable format
def view_lib():
    print("\n- Your Library\n")

    if len(books) == 0:
        print("Your library is empty.")
        return

    for book in books:
        print(book[0], "by", book[1])

    print()

# Define a function that allows the user to add a new book, it asks the user for a title and author using the input function, stores the book as a tuple, adds it to the books list, and also adds the author to the authors set
def add_book():
    print("\n- Add a Book\n")

    print("Enter the title:")
    title = sp_input(False, False, str)

    print("Enter the author:")
    author = sp_input(False, False, str)

    books.append((title, author))
    authors_set.add(author)

    print("\nYou have added")
    print(title, "by", author)
    print()

# Define a function that removes a book from the library, it first displays all books as a numbered list, the user selects a number which corresponds to the book's index, and the selected book is removed from the list using pop
def remove_book():
    print("\n- Remove a Book\n")

    if len(books) == 0:
        print("No books to remove.")
        return

    for i in range(len(books)):
        print(i + 1, ".", books[i][0], "by", books[i][1])

    print("\nEnter the number of the book you want to remove:")
    choice = sp_input(True, list(range(1, len(books) + 1)), int)

    removed = books.pop(choice - 1)

    print("\nYou have removed")
    print(removed[0], "by", removed[1])
    print()

# Define a function that searches the library, the user chooses whether to search by title or author, a keyword is entered and compared to each book using partial matching, and any matching results are printed
def search_lib():
    print("\n- Search Library\n")

    print("What would you like to search by?")
    print("1. Title")
    print("2. Author")

    choice = sp_input(True, [1, 2], int)

    if choice == 1:
        print("\nEnter title keyword:")
        keyword = sp_input(False, False, str).lower()

        for book in books:
            if keyword in book[0].lower():
                print(book[0], "by", book[1])

    elif choice == 2:
        print("\nEnter author name:")
        keyword = sp_input(False, False, str).lower()

        for book in books:
            if keyword in book[1].lower():
                print(book[0], "by", book[1])

    print()

# Define a main function that controls the entire program, displays the menu and runs in a while True loop, based on the user's choice it calls the correct function, and the loop only ends when the user chooses to exit
def main_menu():
    print("Welcome to your Personal Library!")

    while True:
        print("\nType the number for the action you would like to perform\n")
        print("1. View")
        print("2. Add")
        print("3. Remove")
        print("4. Search")
        print("5. Exit")

        choice = sp_input(True, [1, 2, 3, 4, 5], int)

        if choice == 1:
            view_lib()
        elif choice == 2:
            add_book()
        elif choice == 3:
            remove_book()
        elif choice == 4:
            search_lib()
        elif choice == 5:
            print("\nGoodbye!")
            break

# Run the program by calling the main menu function
main_menu()

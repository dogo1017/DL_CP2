"""
Complete Lab 4 and update the following information:

Author: Douglas London
Date: 5/18
"""
class Book:
    def __init__(self, title, author):
        self._title = title
        self._author = author

    def __str__(self):
        return f"{self._title} by {self._author}"


    # Part 1: title property using property() function

    def get_title(self):
        return self._title

    def set_title(self, value):
        # make sure the input is actually a string
        if not isinstance(value, str):
            raise TypeError("Title must be a string.")
        # make sure the string is not empty
        if value == "":
            raise ValueError("Title cannot be empty.")
        self._title = value

    title = property(get_title, set_title)


    # Part 2: author property using @property decorator

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        # make sure the input is actually a string
        if not isinstance(value, str):
            raise TypeError("Author must be a string.")
        # make sure the string is not empty
        if value == "":
            raise ValueError("Author cannot be empty.")
        self._author = value


    # Part 3: read-only description property

    @property
    def description(self):
        return f"{self._title} was written by {self._author}."


def main():
    my_book = Book("Book", "Author")

    # Part 1: update title
    my_book.title = "Harry Potter"

    # Part 2: update author and print
    my_book.author = "J.K. Rowling"
    print(my_book)

    # Part 3: print description, then try to modify it
    print(my_book.description)

    try:
        my_book.description = f"{my_book.title} is a book written by {my_book.author}"
    except AttributeError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
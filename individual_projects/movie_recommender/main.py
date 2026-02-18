# DL Personal Library Manager

# Stores movies, books, albums, etc. as a list of dictionaries
# Data is saved to and loaded from a CSV file so it persists between runs

import csv
import os

# The library is a list where each item is a dictionary
library = []
unsaved_changes = False
filepath = ""

# Fields used for every item in the library
FIELDS = ["title", "creator", "year", "genre", "format", "rating", "notes"]


# Keeps asking the user for input until they type something
# If allow_empty is True, an empty answer is accepted
def ask(prompt, allow_empty=False):
    while True:
        answer = input(prompt).strip()
        if answer != "" or allow_empty:
            return answer
        print("  ! This field can't be empty. Please try again.")


# Keeps asking until the user enters a valid 4-digit year
def ask_year():
    while True:
        answer = input("  Year: ").strip()
        if answer.isdigit() and len(answer) == 4:
            return answer
        print("  ! Please enter a valid 4-digit year (e.g. 2001).")


# Keeps asking until the user types Y or N, returns True for Y and False for N
def ask_yes_no(prompt):
    while True:
        answer = input(prompt + " (Y/N): ").strip().upper()
        if answer == "Y":
            return True
        elif answer == "N":
            return False
        print("  ! Please enter Y or N.")


# Prints a numbered menu and keeps asking until a valid number is entered
# Returns the 0-based index of the chosen option
def ask_menu(options):
    print()
    for i, option in enumerate(options, start=1):
        print(f"  {i}. {option}")
    print()
    while True:
        answer = input("Enter a number: ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return int(answer) - 1
        print(f"  ! Please enter a number between 1 and {len(options)}.")


# Asks the user to pick an item from the library by number
# Returns the 0-based index, or None if the user cancels with 0
def ask_item_number(action):
    if len(library) == 0:
        print("  ! The library is empty.")
        return None
    while True:
        answer = input(f"  Enter item number to {action} (or 0 to cancel): ").strip()
        if answer.isdigit():
            n = int(answer)
            if n == 0:
                return None
            if 1 <= n <= len(library):
                return n - 1
        print(f"  ! Please enter a number between 1 and {len(library)}, or 0 to cancel.")


# Loads items from the CSV file into the library list
# If the file doesn't exist, creates a new empty one with a header row
# Skips any rows that fail to parse and shows a warning
def load_library():
    global library
    library = []

    if not os.path.exists(filepath):
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
        print(f"  No file found, created a new empty library at '{filepath}'.")
        return

    with open(filepath, "r", newline="") as f:
        reader = csv.DictReader(f)
        row_number = 2  # row 1 is the header

        # Maps alternate column names to our standard field names
        # This lets us load CSVs that were made with different headers
        column_aliases = {
            "Title": "title",
            "Director": "creator",
            "Notable Actors": "notes",
            "Length (min)": "format",
            "Rating": "rating",
            "Genre": "genre",
        }

        for row in reader:
            try:
                # Remap any alternate column names to our standard names
                remapped = {}
                for col, value in row.items():
                    standard = column_aliases.get(col, col)
                    remapped[standard] = value

                # Pull each standard field out, defaulting to "" if missing
                item = {}
                for field in FIELDS:
                    item[field] = remapped.get(field, "").strip()

                if item["title"] == "":
                    raise ValueError("missing title")
                library.append(item)
            except Exception as error:
                print(f"  ! Skipping row {row_number} because of an error: {error}")
            row_number += 1


# Writes all items in the library list back to the CSV file
def save_library():
    global unsaved_changes
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(library)
    unsaved_changes = False
    print(f"  Saved {len(library)} item(s) to '{filepath}'.")


# Prints a numbered list showing only title and creator for each item
def show_simple():
    os.system('cls')
    if len(library) == 0:
        print("  (Library is empty.)")
        return
    print()
    for i, item in enumerate(library, start=1):
        print(f"  {i}. {item['title']}  -  {item['creator']}")


# Prints all fields for every item in the library
def show_detailed():
    os.system('cls')
    if len(library) == 0:
        print("  (Library is empty.)")
        return
    print()
    for i, item in enumerate(library, start=1):
        print(f"  {'-' * 40}")
        print(f"  {i}. Title   : {item['title']}")
        print(f"     Creator : {item['creator']}")
        print(f"     Year    : {item['year']}")
        print(f"     Genre   : {item['genre']}")
        if item["format"] != "":
            print(f"     Format  : {item['format']}")
        if item["rating"] != "":
            print(f"     Rating  : {item['rating']}")
        if item["notes"] != "":
            print(f"     Notes   : {item['notes']}")
    print(f"  {'-' * 40}")


# Prompts the user for all item fields and returns a filled dictionary
# If 'existing' is passed in, pressing Enter keeps the current value (used for updates)
def collect_item(existing=None):
    updating = existing is not None
    if updating:
        print("  (Press Enter to keep the current value)")

    # Helper that prompts for one field, handling the update hint and empty check
    def get_field(label, field, required=True):
        hint = f" [{existing[field]}]" if updating and existing[field] != "" else ""
        while True:
            value = input(f"  {label}{hint}: ").strip()
            if value == "" and updating:
                return existing[field]
            if value != "" or not required:
                return value
            print(f"  ! {label} can't be empty.")

    title   = get_field("Title",                        "title")
    creator = get_field("Creator (author/artist/dir.)", "creator")

    # Year is handled separately because it needs digit validation
    while True:
        hint = f" [{existing['year']}]" if updating else ""
        raw = input(f"  Year{hint}: ").strip()
        if raw == "" and updating:
            year = existing["year"]
            break
        if raw.isdigit() and len(raw) == 4:
            year = raw
            break
        print("  ! Please enter a valid 4-digit year.")

    genre  = get_field("Genre",             "genre")
    fmt    = get_field("Format (optional)", "format", required=False)
    rating = get_field("Rating (optional)", "rating", required=False)
    notes  = get_field("Notes (optional)",  "notes",  required=False)

    return {
        "title":   title,
        "creator": creator,
        "year":    year,
        "genre":   genre,
        "format":  fmt,
        "rating":  rating,
        "notes":   notes,
    }


# Asks the user to fill out a new item and adds it to the library
def add_item():
    global unsaved_changes
    os.system('cls')
    print("\n  --- Add Item ---")
    item = collect_item()
    library.append(item)
    unsaved_changes = True
    print(f"  Added '{item['title']}'.")


# Lets the user pick an existing item and edit any of its fields
def update_item():
    global unsaved_changes
    os.system('cls')
    print("\n  --- Update Item ---")
    show_simple()
    index = ask_item_number("update")
    if index is None:
        return
    os.system('cls')
    print(f"\n  Editing: {library[index]['title']}")
    library[index] = collect_item(existing=library[index])
    unsaved_changes = True
    print("  Item updated.")


# Lets the user pick an item to delete, asks for confirmation before removing it
def delete_item():
    global unsaved_changes
    os.system('cls')
    print("\n  --- Delete Item ---")
    show_simple()
    index = ask_item_number("delete")
    if index is None:
        return
    title = library[index]["title"]
    if ask_yes_no(f"  Delete '{title}'?"):
        library.pop(index)
        unsaved_changes = True
        print(f"  Deleted '{title}'.")
    else:
        print("  Deletion cancelled.")


os.system('cls')
print("=" * 50)
print("      Personal Library Manager")
print("=" * 50)

# Use a hardcoded file path for the movie CSV
filepath = "individual_projects/movie_recommender/movies.csv"

# Load the library from the file when the program starts
load_library()

# Menu options shown to the user each loop
MENU = [
    "Show simple list",
    "Show detailed list",
    "Add item",
    "Update item",
    "Delete item",
    "Save library",
    "Reload library from file",
    "Exit",
]

# Main loop - keeps running until the user chooses Exit
while True:
    os.system('cls')
    status = "  [unsaved changes]" if unsaved_changes else ""
    print(f"\n{'-' * 50}")
    print(f"  File: {filepath}  |  Items: {len(library)}{status}")

    choice = ask_menu(MENU)

    if choice == 0:
        show_simple()
    elif choice == 1:
        show_detailed()
    elif choice == 2:
        add_item()
    elif choice == 3:
        update_item()
    elif choice == 4:
        delete_item()
    elif choice == 5:
        os.system('cls')
        save_library()
    elif choice == 6:
        # Warn the user if they have unsaved changes before reloading
        if unsaved_changes:
            if not ask_yes_no("You have unsaved changes. Reload anyway?"):
                continue
        load_library()
        unsaved_changes = False
        print(f"  Reloaded {len(library)} item(s).")
    elif choice == 7:
        # Offer to save before quitting if there are unsaved changes
        if unsaved_changes:
            if ask_yes_no("You have unsaved changes. Save before exiting?"):
                save_library()
        os.system('cls')
        print("\n  Goodbye!\n")
        break
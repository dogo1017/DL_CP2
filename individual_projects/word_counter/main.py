# DL Word Counter
# Reads and writes to a user specified text file
# Tracks word count and timestamps and lets the user view and edit content
# Calls functions from file_handler.py and time_handler.py to do the actual file work
import file_handler
import time_handler
import os

# Clears the screen and prints the main menu options
def show_menu():
    os.system("cls")
    print("  Word Counter")
    print("  ─────────────────────────────────────")
    print("  1.  Update word count")
    print("  2.  View document")
    print("  3.  Add content")
    print("  4.  Edit a line")
    print("  5.  Overwrite document")
    print("  6.  Switch file")
    print("  7.  Exit")
    print("  ─────────────────────────────────────")
    print()

# Prompts the user to type a file path and returns whatever they entered
def get_file_path():
    file_path = input("  Enter the exact file path for your document: ")
    return file_path

# Gets the clean content, counts the words, grabs a timestamp, then writes all of it to the file
# Returns the word count so it can be printed to the screen after
def run_word_count_update(file_path):
    clean_content = file_handler.get_clean_content(file_path)
    word_count = file_handler.count_words(clean_content)
    timestamp = time_handler.get_current_timestamp()
    file_handler.update_document_info(file_path, word_count, timestamp)
    return word_count

# Asks the user to type lines of text one at a time
# Stops collecting when the user presses Enter on an empty line
# Joins all the lines together and returns them as one string
def collect_new_content():
    print()
    print("  Enter new content (press Enter twice to finish):")
    print()
    lines = []
    while True:
        line = input("  ")
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

# file_path starts empty and gets set the first time the user picks any option
file_path = ""

# Main loop that keeps the program running until the user picks Exit
while True:
    show_menu()
    choice = input("  Enter your choice (1-7): ")
    os.system("cls")

    if choice == "1":
        # If no file has been set yet ask for one before doing anything
        if file_path == "":
            file_path = get_file_path()
        word_count = run_word_count_update(file_path)
        print()
        print("  ✔  Word count updated: " + str(word_count) + " words")
        input("\n  Press Enter to continue...")

    elif choice == "2":
        if file_path == "":
            file_path = get_file_path()
        # Reads the full file including the word count and timestamp at the bottom
        content = file_handler.read_document(file_path)
        print()
        print("  ─────────────────────────────────────")
        print(content)
        print("  ─────────────────────────────────────")
        input("\n  Press Enter to continue...")

    elif choice == "3":
        if file_path == "":
            file_path = get_file_path()
        new_content = collect_new_content()
        # Appends the new text then immediately updates the word count so it stays accurate
        file_handler.add_content_to_document(file_path, new_content)
        word_count = run_word_count_update(file_path)
        print()
        print("  ✔  Content added. Word count updated: " + str(word_count) + " words")
        input("\n  Press Enter to continue...")

    elif choice == "4":
        if file_path == "":
            file_path = get_file_path()
        # Gets the content without the word count lines so line numbers stay consistent
        clean_content = file_handler.get_clean_content(file_path)
        lines = clean_content.split("\n")
        print()
        print("  ─────────────────────────────────────")
        line_number = 1
        for line in lines:
            print("  " + str(line_number) + ".  " + line)
            line_number = line_number + 1
        print("  ─────────────────────────────────────")
        print()
        pick = input("  Enter the line number to edit: ")
        # Convert to zero based index since lists start at 0
        index = int(pick) - 1
        print()
        print("  Current:  " + lines[index])
        new_line = input("  New text: ")
        lines[index] = new_line
        updated_content = "\n".join(lines)
        file_handler.write_clean_content(file_path, updated_content)
        print()
        print("  ✔  Line updated successfully.")
        input("\n  Press Enter to continue...")

    elif choice == "5":
        if file_path == "":
            file_path = get_file_path()
        # Collect the new content first so the user does not lose their typing if they go back
        new_content = collect_new_content()
        os.system("cls")
        print()
        print("  ⚠  WARNING: This will erase everything currently in the document.")
        print("  ⚠  This cannot be undone.")
        print()
        print("  1.  Go back (discard what you just typed)")
        print("  2.  Add content instead (keeps existing text)")
        print("  3.  Continue and overwrite")
        print()
        overwrite_choice = input("  Enter your choice (1-3): ")
        os.system("cls")

        if overwrite_choice == "1":
            print("  Overwrite cancelled.")
            input("\n  Press Enter to continue...")

        elif overwrite_choice == "2":
            # Treat it like a normal add so the old text is kept
            file_handler.add_content_to_document(file_path, new_content)
            word_count = run_word_count_update(file_path)
            print()
            print("  ✔  Content added. Word count updated: " + str(word_count) + " words")
            input("\n  Press Enter to continue...")

        elif overwrite_choice == "3":
            # Writes only the new content wiping out everything that was there before
            file_handler.write_clean_content(file_path, new_content)
            word_count = run_word_count_update(file_path)
            print()
            print("  ✔  Document overwritten. Word count: " + str(word_count) + " words")
            input("\n  Press Enter to continue...")

        else:
            print("  ✖  Invalid choice. Returning to menu.")
            input("\n  Press Enter to continue...")

    elif choice == "6":
        # Lets the user point to a different file without restarting the program
        file_path = get_file_path()
        print()
        print("  ✔  File switched successfully.")
        input("\n  Press Enter to continue...")

    elif choice == "7":
        print("  Goodbye!")
        break

    else:
        print()
        print("  ✖  Invalid choice. Please enter a number between 1 and 7.")
        input("\n  Press Enter to continue...")
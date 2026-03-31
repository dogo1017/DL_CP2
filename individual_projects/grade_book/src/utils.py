#DL utils.py

import os


# Clears the terminal then prints a section header with a title
def print_header(title):
    os.system("cls" if os.name == "nt" else "clear")
    print("\n=====================================")
    print(f"  {title}")
    print("=====================================")


# Converts a numerical average to a letter grade string
# Returns N/A if the average is None (no grades entered)
def letter_from_avg(avg):
    if avg is None:
        return "N/A"
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "F"


# Checks that a grade input string is a whole number between 0 and 100
# Returns the integer grade if valid, or None if not
def validate_grade(grade_input):
    if not grade_input.isdigit():
        return None
    grade = int(grade_input)
    if grade < 0 or grade > 100:
        return None
    return grade


# Checks that a grade level input is one of 9, 10, 11, or 12
# Returns the formatted string (e.g. "10th") if valid, or None if not
def validate_grade_level(level_input):
    if level_input not in ["9", "10", "11", "12"]:
        return None
    suffixes = {"9": "9th", "10": "10th", "11": "11th", "12": "12th"}
    return suffixes[level_input]
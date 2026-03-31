#DL menu.py

from utils import print_header, letter_from_avg, validate_grade, validate_grade_level
from student import Student


# Prompts the user to fill out a new student's info, validates each field,
# then adds the student to the gradebook and saves to the CSV
def menu_add_student(gradebook):
    print_header("ADD NEW STUDENT")
    name = input("Enter student name: ").strip()
    student_id = input("Enter student ID: ").strip()

    if gradebook.find_by_id(student_id):
        print("A student with that ID already exists.")
        input("\nPress Enter to continue...")
        return

    grade_level = validate_grade_level(input("Enter grade level (9, 10, 11, 12): ").strip())
    if grade_level is None:
        print("Invalid grade level. Please enter 9, 10, 11, or 12.")
        input("\nPress Enter to continue...")
        return

    student = Student(name, student_id, grade_level)
    gradebook.add_student(student)
    gradebook.save_to_csv()

    print(f"\nStudent added successfully!")
    print(f"  Name:        {name}")
    print(f"  ID:          {student_id}")
    print(f"  Grade Level: {grade_level}")
    print(f"  Grades:      None yet")
    input("\nPress Enter to continue...")


# Shows the current student list, asks the user to pick one by ID,
# validates the grade input, then saves the updated data to CSV
def menu_add_grade(gradebook):
    print_header("ADD GRADE")

    if len(gradebook.students) == 0:
        print("No students in the grade book yet.")
        input("\nPress Enter to continue...")
        return

    print("Current Students:")
    for s in gradebook.students:
        print(f"  - {s.name} (ID: {s.student_id})")

    student_id = input("\nEnter student ID: ").strip()
    student = gradebook.find_by_id(student_id)
    if student is None:
        print("Student not found.")
        input("\nPress Enter to continue...")
        return

    grade = validate_grade(input("Enter grade (0-100): ").strip())
    if grade is None:
        print("Invalid grade. Must be a number between 0 and 100.")
        input("\nPress Enter to continue...")
        return

    student.add_grade(grade)
    gradebook.save_to_csv()

    avg = student.get_average()
    print(f"\nGrade added successfully!")
    print(f"  {student.name} now has {len(student.grades)} grade(s)")
    print(f"  Current average: {avg:.1f} ({student.get_letter_grade()})")
    input("\nPress Enter to continue...")


# Asks for a student ID and prints that student's full record if found
def menu_view_student(gradebook):
    print_header("VIEW STUDENT RECORD")

    if len(gradebook.students) == 0:
        print("No students in the grade book yet.")
        input("\nPress Enter to continue...")
        return

    student_id = input("Enter student ID: ").strip()
    student = gradebook.find_by_id(student_id)
    if student is None:
        print("Student not found.")
        input("\nPress Enter to continue...")
        return

    print()
    student.display()
    input("\nPress Enter to continue...")


# Prints a formatted table of every student with their average, letter grade, and standing
def menu_view_all(gradebook):
    print_header("ALL STUDENTS")

    if len(gradebook.students) == 0:
        print("No students in the grade book yet.")
        input("\nPress Enter to continue...")
        return

    print(f"{'ID':<10} {'Name':<20} {'Avg':<8} {'Grade':<6} {'Standing'}")
    print("-" * 62)
    for s in gradebook.students:
        avg = s.get_average()
        avg_str = f"{avg:.1f}" if avg is not None else "N/A"
        print(f"{s.student_id:<10} {s.name:<20} {avg_str:<8} {s.get_letter_grade():<6} {s.get_academic_standing()}")

    print(f"\nTotal Students: {len(gradebook.students)}")
    input("\nPress Enter to continue...")


# Calculates and displays the overall class average, highest grade, and lowest grade
def menu_class_summary(gradebook):
    print_header("CLASS SUMMARY")

    if len(gradebook.students) == 0:
        print("No students in the grade book yet.")
        input("\nPress Enter to continue...")
        return

    avg = gradebook.get_class_average()
    avg_str = f"{avg:.1f}" if avg is not None else "N/A"
    high = gradebook.get_highest_grade()
    low = gradebook.get_lowest_grade()

    print(f"  Total Students: {len(gradebook.students)}")
    print(f"  Class Average:  {avg_str} ({letter_from_avg(avg)})")
    print(f"  Highest Grade:  {high if high is not None else 'N/A'}")
    print(f"  Lowest Grade:   {low if low is not None else 'N/A'}")
    input("\nPress Enter to continue...")
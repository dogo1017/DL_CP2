#DL gradebook.py

import csv
import os
from student import Student


class GradeBook:
    # Sets up the gradebook with an empty students list and stores the csv path on the object
    def __init__(self, csv_path):
        self.students = []
        self.csv_path = csv_path

    # Adds a Student object to the students list
    def add_student(self, student):
        self.students.append(student)

    # Loops through students and returns the one whose ID matches, or None if not found
    def find_by_id(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    # Loops through students and returns the one whose name matches (case-insensitive), or None
    def find_by_name(self, name):
        for student in self.students:
            if student.name.lower() == name.lower():
                return student
        return None

    # Collects every grade from every student and returns the overall average
    # Returns None if no grades have been entered at all
    def get_class_average(self):
        all_grades = []
        for student in self.students:
            all_grades.extend(student.grades)
        if len(all_grades) == 0:
            return None
        return sum(all_grades) / len(all_grades)

    # Returns the single highest grade across all students, or None if no grades exist
    def get_highest_grade(self):
        all_grades = []
        for student in self.students:
            all_grades.extend(student.grades)
        if len(all_grades) == 0:
            return None
        return max(all_grades)

    # Returns the single lowest grade across all students, or None if no grades exist
    def get_lowest_grade(self):
        all_grades = []
        for student in self.students:
            all_grades.extend(student.grades)
        if len(all_grades) == 0:
            return None
        return min(all_grades)

    # Writes every student and their grades to the CSV file, overwriting what was there
    # Grades are stored as a semicolon-separated string in one column (e.g. "85;92;78")
    def save_to_csv(self):
        with open(self.csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["student_id", "name", "grade_level", "grades"])
            for student in self.students:
                grades_str = ";".join(str(g) for g in student.grades)
                writer.writerow([student.student_id, student.name, student.grade_level, grades_str])

    # Reads the CSV file and rebuilds the students list from it
    # If the file doesn't exist yet, does nothing and returns early
    # Splits the grades column back into a list of integers for each student
    def load_from_csv(self):
        if not os.path.exists(self.csv_path):
            return
        with open(self.csv_path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                student = Student(row["name"], row["student_id"], row["grade_level"])
                if row["grades"]:
                    for g in row["grades"].split(";"):
                        student.add_grade(int(g))
                self.students.append(student)
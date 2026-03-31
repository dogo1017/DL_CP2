#DL student.py


class Student:
    # Sets up a new student with a name, ID, grade level, and an empty grades list
    def __init__(self, name, student_id, grade_level):
        self.name = name
        self.student_id = student_id
        self.grade_level = grade_level
        self.grades = []

    # Appends a single grade to the student's grades list
    def add_grade(self, grade):
        self.grades.append(grade)

    # Returns the average of all grades, or None if there are no grades yet
    def get_average(self):
        if len(self.grades) == 0:
            return None
        return sum(self.grades) / len(self.grades)

    # Converts the numerical average into a letter grade A through F
    # Returns N/A if the student has no grades
    def get_letter_grade(self):
        avg = self.get_average()
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

    # Returns a standing label based on the student's average
    # Honor Roll = 90+, Good Standing = 80-89, Needs Improvement = below 80
    def get_academic_standing(self):
        avg = self.get_average()
        if avg is None:
            return "No Grades"
        if avg >= 90:
            return "Honor Roll"
        elif avg >= 80:
            return "Good Standing"
        else:
            return "Needs Improvement"

    # Prints all of the student's info in a formatted block
    def display(self):
        avg = self.get_average()
        avg_str = f"{avg:.1f}" if avg is not None else "N/A"
        print(f"  Name:              {self.name}")
        print(f"  ID:                {self.student_id}")
        print(f"  Grade Level:       {self.grade_level}")
        print(f"  Grades:            {self.grades if self.grades else 'None yet'}")
        print(f"  Average:           {avg_str} ({self.get_letter_grade()})")
        print(f"  Academic Standing: {self.get_academic_standing()}")
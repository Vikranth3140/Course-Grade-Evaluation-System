import time
import logging

class GradeCalculator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.weights = [("labs", 30), ("midsem", 15), ("assignments", 30), ("endsem", 25)]
        self.policy = [80, 65, 50, 40]
        self.students_data = {}
        self.percentages = {}

    def read_students_data(self):
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    data = line.strip().split(', ')
                    roll_no = int(data[0])
                    marks = list(map(int, data[1:]))
                    self.students_data[roll_no] = marks
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error: File '{self.file_path}' not found.") from e
        except Exception as e:
            raise Exception(f"An unexpected error occurred while reading data: {e}") from e

    def calculate_percentages(self):
        percentages = {}
        for roll_no, marks in self.students_data.items():
            weighted_sum = sum(mark * weight[1] / 100 for mark, weight in zip(marks, self.weights))
            percentages[roll_no] = round(weighted_sum, 2)
        return percentages

    def calculate_grades(self, percentages):
        grades = {}
        for roll_no, percentage in percentages.items():
            grade = self.get_grade(percentage)
            grades[roll_no] = grade
        return grades

    def get_grade(self, percentage):
        if percentage > 80:
            return 'A'
        elif 80 >= percentage > 65:
            return 'B'
        elif 65 >= percentage > 50:
            return 'C'
        elif 50 >= percentage > 40:
            return 'D'
        else:
            return 'F'

    def update_policy(self):
        for i in range(len(self.policy)):
            temp_list = [j for j in self.percentages.values() if abs(self.policy[i] - j) <= 2]
            if temp_list:
                temp_list.sort(reverse=True)
                diff = [temp_list[l - 1] - temp_list[l] for l in range(1, len(temp_list))]
                if diff:
                    self.policy[i] = round((temp_list[diff.index(max(diff))] + temp_list[diff.index(max(diff)) + 1]),
                                           2) / 2

class Student:
    def __init__(self, calculator):
        self.calculator = calculator
        self.grades = {}
        self.percentages = {}
        self.dict_count = {}

    def calculate_statistics(self):
        self.calculator.read_students_data()
        self.percentages = self.calculator.calculate_percentages()  # Moved this line
        self.calculator.update_policy()
        self.grades = self.calculator.calculate_grades(self.percentages)
        self.calculate_grade_counts()

    def calculate_grade_counts(self):
        grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for grade in self.grades.values():
            grade_counts[grade] += 1
        self.dict_count = grade_counts

    def display_course_summary(self):
        print('Course Name:', course_name)
        print('Credits:', credits)
        print('Weights:', self.calculator.weights)
        print('Cutoffs for different grades:', self.calculator.policy)
        print('Grading Summary:', self.dict_count)

    def show_grades(self):
        with open("Student's Grade Summary", "w") as f:
            for roll_no, grade in self.grades.items():
                f.write(f"{roll_no}, {self.percentages[roll_no]}, {grade}\n")

    def search_student_record(self, roll_no):
        if roll_no in self.calculator.students_data:
            print(f'The Marks: {self.calculator.students_data[roll_no]}')
            print(f'The Grade: {self.grades[roll_no]}')
            print(f'The Percentage: {self.percentages[roll_no]}')
        else:
            print('Student with that Roll No not found')

if __name__ == "__main__":
    # Input from user
    course_name = input('Enter Course Name: ')
    credits = int(input('Enter Credits: '))
    file_path = input('Enter file path: ')

    # Initialize GradeCalculator and Student instances
    calculator = GradeCalculator(file_path)
    student_instance = Student(calculator)

    # Perform calculations and display options
    student_instance.calculate_statistics()
    while True:
        print("1. Generate summary of the course")
        print("2. Show the grades of all students")
        print("3. Search student's record")
        choice = input('Enter your choice (press Enter to exit): ')
        if choice == '1':
            student_instance.display_course_summary()
        elif choice == '2':
            student_instance.show_grades()
        elif choice == '3':
            roll_no = int(input("Enter Roll No.: "))
            student_instance.search_student_record(roll_no)
        elif not choice:
            print('Thank You!!!')
            break
        else:
            print('Enter a valid choice')
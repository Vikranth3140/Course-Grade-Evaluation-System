from tabulate import tabulate
import logging

# Configure logging
logging.basicConfig(filename='grad_eval.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

class GradeCalculator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.weights = [("labs", 30), ("midsem", 15), ("assignments", 30), ("endsem", 25)]
        self.policy = [80, 65, 50, 40]
        self.students_data = {}
        self.percentages = {}

    def read_students_data(self):
        logging.info(f"Reading data from file: {self.file_path}")
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    data = line.strip().split(', ')
                    roll_no = int(data[0])
                    marks = list(map(int, data[1:]))
                    self.students_data[roll_no] = marks
        except FileNotFoundError as e:
            logging.error(f"Error: File '{self.file_path}' not found.")
            raise e
        except Exception as e:
            logging.error(f"An unexpected error occurred while reading data: {e}")
            raise e

    def calculate_percentages(self):
        logging.info("Calculating percentages.")
        percentages = {}
        for roll_no, marks in self.students_data.items():
            weighted_sum = sum(mark * weight[1] / 100 for mark, weight in zip(marks, self.weights))
            percentages[roll_no] = round(weighted_sum, 2)
        self.percentages = percentages
        return percentages

    def calculate_grades(self, percentages):
        logging.info("Calculating grades.")
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
        logging.info("Updating policy.")
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
        logging.info("Calculating statistics.")
        self.calculator.read_students_data()
        self.percentages = self.calculator.calculate_percentages()
        self.calculator.update_policy()
        self.grades = self.calculator.calculate_grades(self.percentages)
        self.calculate_grade_counts()

    def calculate_grade_counts(self):
        logging.info("Calculating grade counts.")

        grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for grade in self.grades.values():
            grade_counts[grade] += 1
        self.dict_count = grade_counts

    def display_course_summary(self):
        logging.info("Displaying course summary.")
        file_path = "Course Summary"

        headers = ["Course", "Credits", "Component", "Weightage", "Cutoffs", "Grading Summary"]
        data = []

        for i in range(len(self.calculator.weights)):
            weight_name, weight_value = self.calculator.weights[i]
            cutoff = self.calculator.policy[i]
            grade = chr(ord('A') + i)
            grade_count = self.dict_count[grade]
            data.append([course_name, credits, weight_name, f"{weight_value}%", cutoff, f"{grade} = {grade_count}"])

        f_grade_count = self.dict_count["F"]
        total_weight = sum(weight for _, weight in self.calculator.weights)
        total_students = sum(self.dict_count.values())
        data.append(["", "", "", "", "", f"F = {f_grade_count}"])
        data.append(["", "", "", "", "", ""])
        data.append(["Total", "", "", f"{total_weight}%", "", f"{total_students}"])

        with open(file_path, 'w') as f:
            f.write(tabulate(data, headers=headers, tablefmt="grid"))

        print()
        print(f"Course Summary written to '{file_path}'.")

    def show_grades(self):
        logging.info("Showing grades.")
        file_path = "Students' Grade Summary.txt"

        with open(file_path, "w") as f:
            data = [(roll_no, self.percentages[roll_no], grade) for roll_no, grade in self.grades.items()]
            f.write(tabulate(data, headers=["Student ID", "Total Marks", "Grade"], tablefmt="grid"))

        print()
        print(f"Students Grade Summary written to '{file_path}'.")

    def search_student_record(self, roll_no):
        logging.info(f"Searching for student with Roll No.: {roll_no}")
        if roll_no in self.calculator.students_data:
            
            # Get component names and weights
            component_names = [weight[0] for weight in self.calculator.weights]
            component_weights = [f"{weight[1]}%" for weight in self.calculator.weights]

            # Display individual marks using tabulate
            individual_marks = [["Subject", "Marks"]]
            individual_marks.extend(list(zip(component_names, self.calculator.students_data[roll_no])))
            print(tabulate(individual_marks, headers="firstrow", tablefmt="grid"))

            # Write details to "Student's Grade Record" file
            with open("Student's Grade Record", "w") as f:
                f.write(f"Student ID: {roll_no}\n\n")
                f.write(tabulate(individual_marks, headers="firstrow", tablefmt="grid"))
                f.write(f'\n\nThe Grade: {self.grades[roll_no]}\n')
                f.write(f'The Percentage: {self.percentages[roll_no]}\n')
        else:
            print('Student with that Roll No not found')
            logging.warning(f"Student with Roll No. {roll_no} not found.")


if __name__ == "__main__":
    # Input from user
    print()
    print('Welcome to Grade Evaluation System')
    print()
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
        print()
        choice = input('Enter your choice (press Enter to exit): ')
        if choice == '1':
            print()
            student_instance.display_course_summary()
        elif choice == '2':
            print()
            student_instance.show_grades()
        elif choice == '3':
            print()
            roll_no = int(input("Enter Roll No.: "))
            student_instance.search_student_record(roll_no)
        elif not choice:
            print()
            print('Thank You!!!')
            break
        else:
            print('Enter a valid choice')
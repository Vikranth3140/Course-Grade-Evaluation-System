from tabulate import tabulate
import logging

# Configure logging
logging.basicConfig(filename='grad_eval.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

class GradeCalculator:
    def __init__(self, file_path):
        # Make your changes here
        self.file_path = file_path
        self.weights = [("Labs", 30), ("Midsem", 15), ("Assignments", 30), ("Endsem", 25)]
        self.policy = [80, 65, 50, 40]
        self.students_data = {}
        self.percentages = {}

    def read_students_data(self):
        logging.info("Reading students' data.")
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    data = line.strip().split(', ')
                    roll_no = int(data[0])
                    marks = list(map(int, data[1:]))
                    self.students_data[roll_no] = marks
                    logging.info(f"Succesfully read data for Roll No. {roll_no}.")
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
        logging.info("Percentages calculated.")
        return percentages

    def calculate_grades(self, percentages):
        logging.info("Calculating grades.")

        grades = {}
        for roll_no, percentage in percentages.items():
            grade = self.get_grade(percentage)
            grades[roll_no] = grade
        logging.info("Grades calculated.")
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
                else:
                    self.policy[i] = temp_list[0]
            else:
                self.policy[i] = self.policy[i]
        logging.info("Policy updated.")

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
        logging.info("Statistics calculated.")

    def calculate_grade_counts(self):
        logging.info("Calculating grade counts.")

        grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for grade in self.grades.values():
            grade_counts[grade] += 1
        self.dict_count = grade_counts
        logging.info("Grade counts calculated.")

    def display_course_summary(self):
        file_path = "Course Summary.txt"

        headers = ["Component", "Weightage", "Cutoffs", "Grading Summary"]
        data = []

        for i in range(len(self.calculator.weights)):
            weight_name, weight_value = self.calculator.weights[i]
            cutoff = self.calculator.policy[i]
            grade = chr(ord('A') + i)
            grade_count = self.dict_count[grade]
            data.append([weight_name, f"{weight_value}%", cutoff, f"{grade} = {grade_count}"])

        # Add a row for "F" grade
        f_grade_count = self.dict_count["F"]
        data.append(["", "", "", f"F = {f_grade_count}"])

        # Add a row for total components
        total_components_row = ["", "", "", ""]
        data.append(total_components_row)

        total_weight = sum(weight for _, weight in self.calculator.weights)
        total_students = sum(self.dict_count.values())

        # Add a row for the final summary
        total_row = ["Total", f"{total_weight}%", "", f"{total_students}"]
        data.append(total_row)

        # Write to file
        with open(file_path, 'w') as f:
            f.write(f"Course: {course_name}\n")
            f.write(f"Credits: {credits}\n\n")
            f.write(tabulate(data, headers=headers, tablefmt="grid"))

        print(f"Course Summary written to '{file_path}'.")
        logging.info(f"Course Summary written to '{file_path}'.")

    def show_grades(self):
        file_path = "Students' Grade Summary.txt"

        with open(file_path, "w") as f:
            data = [(roll_no, self.percentages[roll_no], grade) for roll_no, grade in self.grades.items()]
            f.write(tabulate(data, headers=["Student ID", "Total Marks", "Grade"], tablefmt="grid"))

        print()
        print(f"Students' Grade Summary written to '{file_path}'.")
        print()
        logging.info(f"Students' Grade Summary written to '{file_path}'.")

    def search_student_record(self, roll_no):
        logging.info(f"Searching for student with Roll No.: {roll_no}")
        if roll_no in self.calculator.students_data:
            
            # Get component names and weights
            component_names = [weight[0] for weight in self.calculator.weights]
            component_weights = [f"{weight[1]}%" for weight in self.calculator.weights]

            # Display individual marks using tabulate
            individual_marks = [["Component", "Marks"]]
            individual_marks.extend(list(zip(component_names, self.calculator.students_data[roll_no])))

            # Write details to "Student's Grade Record" file
            file_path = "Student's Grade Summary.txt"
            with open(file_path, "w") as f:
                f.write(f"Student ID: {roll_no}\n\n")
                f.write(tabulate(individual_marks, headers="firstrow", tablefmt="grid"))
                f.write(f'\n\nGrade: {self.grades[roll_no]}\n')
                f.write(f'Percentage: {self.percentages[roll_no]}\n')
                logging.info(f"Student with Roll No. {roll_no} found.")
                print()
                print(f"Student's Grade Record written to '{file_path}'.")
                print()
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
        print()
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
            print()
            break
        else:
            print('Enter a valid choice')
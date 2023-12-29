class Student:
    def __init__(self, student_id, marks):
        self.student_id = student_id
        self.marks = marks

class GradeCalculator:
    def __init__(self, weights):
        self.weights = weights

    def calculate_weighted_sum(self, student):
        weighted_sum = sum(mark * weight[1] / weight[0] for mark, weight in zip(student.marks, self.weights))
        return weighted_sum

    def calculate_grade(self, total_marks):
        if total_marks > 80:
            return 'A'
        elif 80 >= total_marks > 70:
            return 'A-'
        elif 70 >= total_marks > 60:
            return 'B'
        elif 60 >= total_marks > 50:
            return 'B-'
        elif 50 >= total_marks > 40:
            return 'C'
        elif 40 >= total_marks > 35:
            return 'C-'
        elif 35 >= total_marks > 30:
            return 'D'
        else:
            return 'F'

def read_student_data(file_path):
    students = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                student_id = int(data[0])
                marks = list(map(int, data[1:]))
                students.append(Student(student_id, marks))
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred while reading data: {e}")
    return students

def write_grade_data(students, grade_calculator, output_file_path):
    try:
        with open(output_file_path, 'w') as file:
            file.write("Student ID, Total Marks, Grade\n\n")
            for student in students:
                weighted_sum = grade_calculator.calculate_weighted_sum(student)
                total_marks = round(weighted_sum, 2)
                grade = grade_calculator.calculate_grade(total_marks)
                file.write(f"{student.student_id}, {total_marks}, {grade}\n")
    except Exception as e:
        print(f"An unexpected error occurred while writing data: {e}")

def main():
    try:
        weights = [(10, 5), (20, 5), (100, 15), (40, 10), (100, 35), (100, 30)]
        students = read_student_data("IPmarks.txt")
        if students:
            print("Student data loaded successfully.")
            grade_calculator = GradeCalculator(weights)
            write_grade_data(students, grade_calculator, "IPgrade.txt")
            print("Grade data written successfully to 'IPgrade.txt'.")
        else:
            print("No student data found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
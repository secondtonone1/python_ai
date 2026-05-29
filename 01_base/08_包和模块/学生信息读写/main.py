from info_utils import read_students_csv, calculate_average, save_report
if __name__ == '__main__':
    students = read_students_csv('students.csv')
    print(students)
    print(calculate_average(students))
    save_report('./students.json',students)


import csv
import json

def read_students_csv(filename):
    '''
    读取学生信息
    :param filename: 文件名, students.csv
    :return: 返回列表[], 每个元素是 json格式，存储学生信息
    {
        'name': zack,
        'age': 25,
        'score':9.9
    }
    '''
    students = []
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append(
                    {
                        'name': row['name'],
                        'age': int(row['age']),
                        'score': float(row['score'])
                    }
                )
        return students
    except Exception as e:
        print(f'文件读取错误,error is {e}')
        return []

def calculate_average(students):
    '''
    计算平均值
    :param students: 传入的学生列表，每个元素是一个字典
    :return: 所有学生的平均值
    '''
    if not students:
        return 0
    total = sum(s['score'] for s in students)
    return total / len(students)

def find_top_student(students):
    '''
    查找成绩最高的学生的信息
    :param students: [{'score':100,'name':'zack','age':25},
    {'score':95,'name':'bob','age':30}]
    :return: 返回分数最高的学生信息
    '''
    if not students:
        return None
    return max(students, key = lambda s: s['score'])

def save_report(filename, students):
    '''
    将字典信息存储为json文件
    :param filename: json文件的路径
    :param students: 学生信息  [{'score':100,'name':'zack','age':25},
    {'score':95,'name':'bob','age':30}]
    :return: None
    '''
    try:
        report = {
            'total_students': len(students),
            'average_students': calculate_average(students),
            'top_students': find_top_student(students),
            'students': students
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent = 2, ensure_ascii=False)
        print(f'报告已经保存到{filename}')
    except Exception as e:
        print(f'错误，,error is {e}')

if __name__ == '__main__':
    students = read_students_csv('../students.csv')
    print(students)
    print(calculate_average(students))
    save_report('./students.json',students)
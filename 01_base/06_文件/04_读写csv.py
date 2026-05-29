'''
演示文件读写
'''

'''
演示csv读写
'''
def read_csv_example(filename):
    with open(filename,'r',encoding='utf-8') as f:
        header_line = f.readline()
        print(f'表头信息: ', header_line)
        index = 1
        for line in f:
            # 去掉末尾的\n换行符
            new_str = line.rstrip('\n')
            # 返回数据列表，按照,切割字符串
            data_list = new_str.split(',')
            print(f'第{index}行数据为: ', data_list)

# 写csv
def write_csv(filename, students):
    '''

    :param filename: 文件路径
    :param students: students学生列表，
    每个元素是一个字典[{'name':'zack','age':25},{'name':'ray','age':24}]
    :return: None
    '''
    with open(filename,'w',encoding='utf-8') as f:
        # 先写表头
        f.write('name,age,score\n')
        # 循环写数据体
        for student in students:
            line = f"{student['name']},{student['age']},{student['score']}\n"
            f.write(line)

# 读取csv
def read_csv(filename):
    '''

    :param filename: 文件名
    :return: students学生列表，
    每个元素是一个字典[{'name':'zack','age':25},{'name':'ray','age':24}]
    '''
    students = []
    with open(filename,'r',encoding='utf-8') as f:
        # 掠过表头
        f.readline()
        # 读取内容
        for line in f:
            data_list = line.rstrip('\n').split(',')
            data_dict = {
                'name':data_list[0],
                'age':data_list[1],
                'score':data_list[2]
            }
            students.append(data_dict)
    return students



if __name__ == '__main__':
    #read_csv_example('./male_file.csv')
    students = [{'name':'zack','age':25,'score':100},{'name':'ray','age':24,'score':150}]
    write_csv('students.csv',students)
    print(read_csv(filename='students.csv'))
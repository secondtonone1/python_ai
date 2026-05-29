'''
简易成绩管理系统
功能:
1.输入学生姓名和三门科目成绩
2. 计算总分和平均分
3. 根据平均分进行成绩评级
4. 格式化输出所有信息
'''
# 输入学生信息
student_name = input('请输入学生姓名: ')
chinese_str = input('请输入语文成绩: ')
math_str = input('请输入数学成绩: ')
english_str = input('请输入英语成绩: ')

# 类型转换(处理输入的字符串, 转化为浮点数)
chinese = float(chinese_str)
math = float(math_str)
english = float(english_str)

# 计算总分
total_score = chinese + math + english
# 平均分
avg_score = total_score/3

# 根据平均分评级
if avg_score >= 90:
    grade = '优秀'
elif avg_score >= 80:
    grade = '良好'
elif avg_score >= 70:
    grade = '中等'
elif avg_score >= 60:
    grade = '及格'
else:
    grade = '不及格'

print('='*40)
print(f'学生姓名: {student_name}')
print(f'语文成绩: {chinese:.1f}分')
print(f'数学成绩: {math:.1f}分')
print(f'英语成绩: {english:.1f}分')
print(f'总成绩: {total_score:.1f}分')
print(f'平均成绩: {avg_score:.1f}分')
print(f'成绩评级: {grade}')
print('='*40)

'''
班级活动费用分摊系统
功能:
1.输入参与人数和活动总花费
2. 额外收取10%组织管理费用，计算最终总费用
3. 判断人数是否合法(至少1人)
4. 计算每人要分摊的金额并输出
'''

# 输入并转换数据类型
total_people = int(input('请输入参与活动的人数: '))
total_col = float(input('请输入活动总花费(元): '))

# 条件判断,人数是否合法
if total_people < 1:
    print('人数输入错误，至少1人')
else:
    # 计算增加组织管理费后的总费用以及人均费用
    manage_fee = total_col * 0.1
    final_col = total_col + manage_fee
    # 计算人均费用
    per_people_col = final_col / total_people

    # 格式化输出
    print("=" * 30)
    print(f"原始活动花费：{total_col:.2f}元")
    print(f"10%组织管理费：{manage_fee:.2f}元")
    print(f"最终总费用：{final_col:.2f}元")
    print(f"参与人数：{total_people}人")
    print(f"每人需分摊：{per_people_col:.2f}元")
    print("=" * 30)
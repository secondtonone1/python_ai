import pymysql
from pymysql.cursors import DictCursor
# 1. 创建数据库连接对象
def init_db():
    conn = pymysql.connect(
        host='119.91.129.93',
        port = 3308,
        user= 'root',
        password='123456',
        database='py_adv_db',
        charset='utf8mb4'
    )
    return conn

def insert_usr_info(cursor,  data ):
    sql = """
    insert into user(name,age,email) values(%s,%s,%s)
    """
    # 参数列表
    # 执行语句
    cursor.execute(sql,data)
    # 提交事务
    conn.commit()
    print(f'受影响的行数: {cursor.rowcount}')

def update_user_info(cursor, age, id ):
    sql = """
    update user set age=%s where id=%s"""
    cursor.execute(sql, (age, id))
    conn.commit()
    print(f'受影响的函数: {cursor.rowcount}')

def delete_user_info(cursor, id ):
    sql = """
    delete from user where id=%s"""
    cursor.execute(sql, (id,))
    conn.commit()

def fetch_one(cursor):
    sql = """
       select * from user 
    """
    cursor.execute(sql)
    row = cursor.fetchone()
    print(row)

def fetch_all(cursor):
    sql = """
       select * from user 
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows)

def fetch_many(cursor,nums):
    sql = """
          select * from user 
    """
    cursor.execute(sql)
    rows = cursor.fetchmany(nums)
    print(rows)

def fetch_one_loop(cursor):
    sql = """
    select * from user 
        """
    cursor.execute(sql)
    while True:
        row = cursor.fetchone()
        if not row:
            break
        print(row)

def sql_execute_dangerous(cursor):
    # zs'or'1=1 是有危险的
    name = input("请输入用户名:")
    sql = f"SELECT * FROM user WHERE name = '{name}'"
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows)

def commit_update(cursor):
    try:
        sql1 = "update user set age=%s where id=%s"
        sql2 = "update user set age=%s where id=%s"
        cursor.execute(sql1,(19,2))
        raise('出现异常')
        cursor.execute(sql2,(13,3))
        conn.commit()
        print('更新成功')
    except Exception as e:
        conn.rollback()
        print(f'更新失败')
    finally:
        # 可以关闭光标和链接等，因为我们在别的函数回收了，所以此处不处理
        print('执行完毕')

def execute_many(cursor, data_list):
    sql = 'INSERT INTO user (name,age,email) VALUES (%s,%s,%s)'
    cursor.executemany(sql, data_list)
    conn.commit()
    print(f'批量插入的行数: {cursor.rowcount}')


def get_cursor(conn):
    return conn.cursor()

def close_cursor(cursor):
    cursor.close()

def close_conn(conn):
    conn.close()

class UserDB:
    def __init__(self):
        self.conn = pymysql.connect(
            host='119.91.129.93',
            user='root',
            password='123456',
            database='py_adv_db',
            charset='utf8mb4',
            port=3308,
        )

    def add_user(self,name,age,email):
        sql = """
        insert into user(name,age,email) values(%s,%s,%s)"""

        with self.conn.cursor() as cursor:
            cursor.execute(sql,(name,age,email))
            self.conn.commit()
            return cursor.lastrowid

    def get_user(self,uid):
        sql = """
        select * from user where id=%s"""

        with self.conn.cursor(DictCursor) as cursor:
            cursor.execute(sql,(uid,))
            return cursor.fetchone()

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    conn = init_db()
    cursor = get_cursor(conn)
    # print(f'cursor is {cursor}')
    # # insert_usr_info(cursor,('张三',22,'zhangsan@163.com'))
    # # update_user_info(cursor,8,1)
    # # delete_user_info(cursor,1)
    # # fetch_one(cursor)
    # # fetch_many(cursor,5)
    # # fetch_all(cursor)
    # # fetch_one_loop(cursor)
    # # sql_execute_dangerous(cursor)
    # execute_many(cursor, [('李四',20,'secondtonone1@qq.com'),
    #                       ('王五',21,'1017232@qq.com'),
    #                       ('赵六',18,'11234@qq.com')])
    # # commit_update(cursor)
    close_cursor(cursor)
    close_conn(conn)
    db = UserDB()
    new_id = db.add_user('小明',8,'xm@qq.com')
    print('新增id: ', new_id)
    print(db.get_user(new_id))
    db.close()
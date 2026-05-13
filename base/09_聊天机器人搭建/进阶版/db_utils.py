"""
数据库操作工具模块
"""

import pymysql
from db_config import DB_CONFIG
import json
from datetime import datetime


class ChatDatabase:
    def __init__(self):
        """初始化数据库连接"""
        self.connection = None
        self.create_database_if_not_exists()
        self.connect()
        self.create_table()

    def create_database_if_not_exists(self):
        """如果数据库不存在则创建"""
        try:
            # 先连接到MySQL服务器（不指定数据库）
            conn = pymysql.connect(
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                charset=DB_CONFIG['charset']
            )
            cursor = conn.cursor()

            # 创建数据库
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"数据库 {DB_CONFIG['database']} 已准备就绪")

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"创建数据库时出错: {e}")

    def connect(self):
        """连接到数据库"""
        try:
            self.connection = pymysql.connect(**DB_CONFIG)
            print("数据库连接成功")
        except Exception as e:
            print(f"数据库连接失败: {e}")
            raise

    def is_connected(self):
        """检查连接是否有效"""
        try:
            if self.connection is None:
                return False
            # 使用 ping() 检测连接是否有效
            self.connection.ping()
            return True
        except Exception as e:
            print(f"连接检测失败: {e}")
            return False

    def reconnect(self):
        """重新连接数据库"""
        try:
            if self.connection:
                try:
                    self.connection.close()
                except:
                    pass
            self.connect()
            print("数据库已重新连接")
            return True
        except Exception as e:
            print(f"重新连接失败: {e}")
            return False

    def create_table(self):
        """创建聊天记录表"""
        try:
            cursor = self.connection.cursor()

            # 创建聊天记录表
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                role VARCHAR(20) NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_timestamp (timestamp)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """

            cursor.execute(create_table_sql)
            self.connection.commit()
            print("数据表已准备就绪")
            cursor.close()
        except Exception as e:
            print(f"创建表时出错: {e}")
            raise

    def save_message(self, role, content):
        """保存单条消息"""
        try:
            # 检查连接是否有效，无效则重连
            if not self.is_connected():
                print("连接已断开，正在重新连接...")
                if not self.reconnect():
                    print("重新连接失败")
                    return False

            cursor = self.connection.cursor()
            sql = "INSERT INTO chat_messages (role, content) VALUES (%s, %s)"
            cursor.execute(sql, (role, content))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"保存消息失败: {e}")
            try:
                self.connection.rollback()
            except:
                # 如果 rollback 也失败，说明连接已断开，标记需要重连
                print("Rollback 失败，连接已断开")
            return False

    def load_all_messages(self, limit=100):
        """加载所有聊天记录（默认最近100条）"""
        try:
            # 检查连接是否有效
            if not self.is_connected():
                print("连接已断开，正在重新连接...")
                if not self.reconnect():
                    print("重新连接失败")
                    return []

            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            sql = """
            SELECT role, content, timestamp 
            FROM chat_messages 
            ORDER BY timestamp ASC 
            LIMIT %s
            """
            cursor.execute(sql, (limit,))
            results = cursor.fetchall()
            cursor.close()

            # 转换为所需格式
            messages = []
            for row in results:
                messages.append({
                    'role': row['role'],
                    'content': row['content']
                })

            return messages
        except Exception as e:
            print(f"加载消息失败: {e}")
            return []

    def clear_all_messages(self):
        """清空所有聊天记录"""
        try:
            # 检查连接是否有效
            if not self.is_connected():
                print("连接已断开，正在重新连接...")
                if not self.reconnect():
                    print("重新连接失败")
                    return False

            cursor = self.connection.cursor()
            cursor.execute("TRUNCATE TABLE chat_messages")
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"清空记录失败: {e}")
            try:
                self.connection.rollback()
            except:
                print("Rollback 失败，连接已断开")
            return False

    def get_message_count(self):
        """获取消息总数"""
        try:
            # 检查连接是否有效
            if not self.is_connected():
                print("连接已断开，正在重新连接...")
                if not self.reconnect():
                    print("重新连接失败")
                    return 0

            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM chat_messages")
            result = cursor.fetchone()
            cursor.close()
            return result[0]
        except Exception as e:
            print(f"获取消息数量失败: {e}")
            return 0

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            try:
                self.connection.close()
                print("数据库连接已关闭")
            except:
                pass


# 测试代码
if __name__ == '__main__':
    db = ChatDatabase()

    # 测试保存消息
    db.save_message('assistant', '你好，我是黑马智聊机器人')
    db.save_message('user', '你好')

    # 测试加载消息
    messages = db.load_all_messages()
    print(f"共有 {len(messages)} 条消息")
    for msg in messages:
        print(f"{msg['role']}: {msg['content']}")

    db.close()
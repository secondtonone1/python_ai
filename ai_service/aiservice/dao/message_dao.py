'''
消息表数据访问对象 (DAO)
'''
from aiservice.common.logger import get_logger
from aiservice.dao.db_pool import DbPool


class MessageDao:
    """t_message 会话消息表"""

    def __init__(self):
        self._logger = get_logger(__name__)

    @property
    def _pool(self) -> DbPool:
        """惰性获取连接池: 真正执行 SQL 时才取单例"""
        return DbPool.instance()

    def add(self, session_id: int, role: str, content: str, source: str | None = None) -> int:
        """写入一条消息, 返回消息 id"""
        sql = 'INSERT INTO t_message (session_id, role, content, source) VALUES (%s, %s, %s, %s)'
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (session_id, role, content, source))
            return cursor.lastrowid

    def list_by_session(self, session_id: int, limit: int = 100) -> list[dict]:
        """查询会话的全部消息(倒序取 limit 条后正序返回, 用于历史记录展示)"""
        sql = ('SELECT id, session_id, role, content, source, rating, created_at '
               'FROM t_message WHERE session_id = %s ORDER BY id DESC LIMIT %s')
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (session_id, limit))
            # 注意: pymysql 对空结果集返回空元组 () 而非空列表, 用 list() 统一转成列表
            rows = list(cursor.fetchall())
        rows.reverse()
        return rows

    def list_after_id(self, session_id: int, after_id: int) -> list[dict]:
        """查询某条消息之后的新消息 (客服工作台轮询用)"""
        sql = ('SELECT id, session_id, role, content, source, rating, created_at '
               'FROM t_message WHERE session_id = %s AND id > %s ORDER BY id')
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (session_id, after_id))
            return cursor.fetchall()

    def rate(self, message_id: int, rating: int) -> int:
        """对消息做满意度评价, 返回受影响行数 (0=消息不存在)"""
        sql = 'UPDATE t_message SET rating = %s WHERE id = %s AND role = %s'
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (rating, message_id, 'bot'))
            return cursor.rowcount

    def bot_stats(self) -> dict:
        """机器人消息统计: 总条数 / 知识库命中数 / 已评价数 / 平均满意度 (报表用)"""
        sql = ('SELECT COUNT(*) AS bot_total, '
               'SUM(CASE WHEN source = %s THEN 1 ELSE 0 END) AS knowledge_hits, '
               'SUM(CASE WHEN rating IS NOT NULL THEN 1 ELSE 0 END) AS rated_count, '
               'AVG(rating) AS avg_rating '
               'FROM t_message WHERE role = %s')
        with self._pool.cursor() as cursor:
            cursor.execute(sql, ('knowledge', 'bot'))
            return cursor.fetchone()

    def count_today(self) -> int:
        """今日消息总量 (报表用)"""
        sql = 'SELECT COUNT(*) AS cnt FROM t_message WHERE created_at >= CURDATE()'
        with self._pool.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()['cnt']

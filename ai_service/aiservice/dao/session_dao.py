'''
会话表数据访问对象 (DAO)
========================
DAO 层职责: 只负责数据库的增删改查, 不掺杂业务逻辑。
所有 SQL 一律参数化(占位符 %s), 杜绝 SQL 注入(对应课程 90 中 sql_execute_dangerous 的反面教材)。
'''
from aiservice.common.constants import SessionStatus
from aiservice.common.logger import get_logger
from aiservice.dao.db_pool import DbPool


class SessionDao:
    """t_session 客服会话表"""

    def __init__(self):
        self._logger = get_logger(__name__)

    @property
    def _pool(self) -> DbPool:
        """惰性获取连接池: 真正执行 SQL 时才取单例,
        这样服务模块在导入阶段不会因"连接池尚未初始化"而崩溃"""
        return DbPool.instance()

    def create(self, visitor_name: str = '访客') -> int:
        """创建会话, 返回会话 id"""
        sql = 'INSERT INTO t_session (visitor_name) VALUES (%s)'
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (visitor_name,))
            return cursor.lastrowid

    def get(self, session_id: int) -> dict | None:
        """查询会话, 不存在返回 None"""
        sql = ('SELECT id, visitor_name, status, created_at, updated_at, closed_at '
               'FROM t_session WHERE id = %s')
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (session_id,))
            return cursor.fetchone()

    def update_status(self, session_id: int, status: str) -> None:
        """更新会话状态"""
        sql = 'UPDATE t_session SET status = %s WHERE id = %s'
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (status, session_id))

    def touch(self, session_id: int) -> None:
        """刷新会话的最后活动时间 (updated_at 由数据库 ON UPDATE 自动维护)"""
        sql = 'UPDATE t_session SET updated_at = NOW() WHERE id = %s'
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (session_id,))

    def close(self, session_id: int) -> None:
        """关闭会话"""
        sql = 'UPDATE t_session SET status = %s, closed_at = NOW() WHERE id = %s'
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (SessionStatus.CLOSED, session_id))

    def list_by_status(self, status: str, limit: int = 50) -> list[dict]:
        """按状态查询会话列表(客服工作台用), 按最后活动时间倒序"""
        sql = ('SELECT id, visitor_name, status, created_at, updated_at '
               'FROM t_session WHERE status = %s ORDER BY updated_at DESC LIMIT %s')
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (status, limit))
            return cursor.fetchall()

    def archive_timeout(self, timeout_minutes: int) -> int:
        """把超时未活动的会话归档, 返回归档条数 (后台任务周期调用)"""
        sql = ('UPDATE t_session SET status = %s '
               'WHERE status IN (%s, %s, %s) AND updated_at < DATE_SUB(NOW(), INTERVAL %s MINUTE)')
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (
                SessionStatus.ARCHIVED,
                SessionStatus.BOT, SessionStatus.WAITING_HUMAN, SessionStatus.HUMAN,
                timeout_minutes,
            ))
            return cursor.rowcount

    def count_by_status(self) -> list[dict]:
        """各状态会话数量 (统计报表用)"""
        sql = 'SELECT status, COUNT(*) AS cnt FROM t_session GROUP BY status'
        with self._pool.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

'''
客服账号表数据访问对象 (DAO)
============================
密码安全实践: 数据库只存 SHA256(盐 + 明文) 的哈希值, 不存明文;
校验时对输入做同样的哈希再比对 (哈希算法不可逆)。
'''
from aiservice.common.logger import get_logger
from aiservice.dao.db_pool import DbPool


class StaffDao:
    """t_staff 客服账号表"""

    def __init__(self):
        self._logger = get_logger(__name__)

    @property
    def _pool(self) -> DbPool:
        """惰性获取连接池: 真正执行 SQL 时才取单例"""
        return DbPool.instance()

    def get_by_username(self, username: str) -> dict | None:
        """按登录名查询客服, 不存在返回 None"""
        sql = 'SELECT id, username, password_hash, display_name FROM t_staff WHERE username = %s'
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (username,))
            return cursor.fetchone()

    def get_by_id(self, staff_id: int) -> dict | None:
        """按主键查询客服 (校验请求头中的客服身份用)"""
        sql = 'SELECT id, username, password_hash, display_name FROM t_staff WHERE id = %s'
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (staff_id,))
            return cursor.fetchone()

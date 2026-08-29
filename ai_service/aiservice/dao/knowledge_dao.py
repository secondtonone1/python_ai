'''
知识库表数据访问对象 (DAO)
==========================
知识库是规则引擎的数据源。后续阶段升级为向量检索(RAG)时,
本层接口保持不变, 只替换底层实现 —— DAO 分层的意义所在。
'''
from aiservice.common.logger import get_logger
from aiservice.dao.db_pool import DbPool


class KnowledgeDao:
    """t_knowledge 客服知识库表"""

    def __init__(self):
        self._logger = get_logger(__name__)

    @property
    def _pool(self) -> DbPool:
        """惰性获取连接池: 真正执行 SQL 时才取单例"""
        return DbPool.instance()

    def list_enabled(self) -> list[dict]:
        """查询所有启用的知识条目 (规则引擎用)"""
        sql = ('SELECT id, category, question, keywords, answer '
               'FROM t_knowledge WHERE enabled = 1')
        with self._pool.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def list_all(self) -> list[dict]:
        """查询全部知识条目 (客服工作台管理用)"""
        sql = ('SELECT id, category, question, keywords, answer, enabled, hit_count, created_at '
               'FROM t_knowledge ORDER BY id')
        with self._pool.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def add(self, category: str, question: str, keywords: str, answer: str) -> int:
        """新增知识条目, 返回条目 id"""
        sql = 'INSERT INTO t_knowledge (category, question, keywords, answer) VALUES (%s, %s, %s, %s)'
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (category, question, keywords, answer))
            return cursor.lastrowid

    def update(self, knowledge_id: int, fields: dict) -> int:
        """按字段更新知识条目 (fields 只包含要更新的列), 返回受影响行数"""
        allowed = {'category', 'question', 'keywords', 'answer', 'enabled'}
        updates = {k: v for k, v in fields.items() if k in allowed}
        if not updates:
            return 0
        set_clause = ', '.join(f'{k} = %s' for k in updates)
        sql = f'UPDATE t_knowledge SET {set_clause} WHERE id = %s'
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (*updates.values(), knowledge_id))
            return cursor.rowcount

    def delete(self, knowledge_id: int) -> int:
        """删除知识条目, 返回受影响行数"""
        sql = 'DELETE FROM t_knowledge WHERE id = %s'
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (knowledge_id,))
            return cursor.rowcount

    def hit_increment(self, knowledge_id: int) -> None:
        """知识条目命中次数 +1 (运营统计)"""
        sql = 'UPDATE t_knowledge SET hit_count = hit_count + 1 WHERE id = %s'
        with self._pool.cursor() as cursor:
            cursor.execute(sql, (knowledge_id,))

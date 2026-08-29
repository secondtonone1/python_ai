'''
数据库连接池模块
================
为什么需要连接池? Web 服务每次请求都新建连接的开销很大(TCP握手 + MySQL认证),
企业项目都用连接池复用连接, 业界最常用的纯 Python 实现是 DBUtils。

在课程 02_advance/90_pymysql操作.py 的基础上引入:
1. DBUtils 连接池 (单例)
2. 上下文管理器自动"提交/回滚/归还" (对应课程 02_advance/21_enter和exit.py)
'''
import threading
from contextlib import contextmanager

import pymysql
from dbutils.pooled_db import PooledDB
from pymysql.cursors import DictCursor

from aiservice.common.logger import get_logger


class DbPool:
    """MySQL 连接池 (单例): 整个服务进程共享一个连接池"""

    _instance = None
    _config: dict | None = None      # 记住数据库配置, 供初始化失败后重试 (DB 恢复自愈)
    _init_lock = threading.RLock()   # 多线程同时触发初始化时只建一次池

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_config: dict | None = None):
        if getattr(self, '_ready', False):
            return
        # 首次调用时记住配置; 之后即使不传配置也能用缓存配置重试初始化
        if db_config is not None:
            DbPool._config = db_config
        if DbPool._config is None:
            raise RuntimeError('连接池未初始化: 首次使用必须调用 DbPool.instance(db_config)')
        with DbPool._init_lock:
            if getattr(self, '_ready', False):
                return
            self._logger = get_logger(__name__)
            # 若数据库瞬时不可用, 这里会抛异常: 只告警不崩溃,
            # 后续每次调用都会重试, 数据库恢复后即可自动建池 (可靠性设计见 docs/02 第 9 章)
            self._pool = PooledDB(
                creator=pymysql,
                maxconnections=int(DbPool._config.get('pool_max', 10)),  # 池中最大连接数
                mincached=int(DbPool._config.get('pool_min', 2)),        # 启动时预创建的连接数
                maxcached=int(DbPool._config.get('pool_max', 10)),
                blocking=True,      # 连接全部被占用时: 阻塞等待而不是直接报错
                host=DbPool._config.get('host'),
                port=int(DbPool._config.get('port', 3306)),
                user=DbPool._config.get('user'),
                password=DbPool._config.get('password'),
                database=DbPool._config.get('db'),
                charset=DbPool._config.get('charset', 'utf8mb4'),
                cursorclass=DictCursor,  # 查询结果以"字典"形式返回, 便于业务层使用
            )
            self._ready = True
            self._logger.info(f'数据库连接池初始化成功: '
                              f'{DbPool._config.get("host")}:{DbPool._config.get("port")}/{DbPool._config.get("db")}')

    @classmethod
    def instance(cls, db_config: dict | None = None) -> 'DbPool':
        """获取连接池单例; 第一次调用必须传入数据库配置"""
        if cls._instance is None and db_config is None and cls._config is None:
            raise RuntimeError('连接池未初始化: 首次使用必须调用 DbPool.instance(db_config)')
        return cls(db_config)

    @contextmanager
    def cursor(self):
        """上下文管理器: 借连接 -> 执行SQL -> 提交/回滚 -> 归还连接。
        使用方式:
            with pool.cursor() as cursor:
                cursor.execute(sql, params)
                rows = cursor.fetchall()
        (对应课程 21_enter和exit.py 上下文管理器)
        """
        conn = self._pool.connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()      # 成功 -> 提交事务
        except Exception:
            conn.rollback()    # 失败 -> 回滚事务
            raise
        finally:
            cursor.close()
            conn.close()       # 归还连接到池中 (不是真正断开物理连接)

    def close(self) -> None:
        """关闭整个连接池 (进程退出时调用)"""
        if getattr(self, '_ready', False):
            self._pool.close()
            self._ready = False
            self._logger.info('数据库连接池已关闭')

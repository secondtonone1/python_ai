'''
统一日志模块
============
企业级项目要求: 所有模块使用统一的日志格式, 同时输出到控制台和文件;
文件日志按大小自动轮转(RotatingFileHandler), 避免日志文件无限膨胀。
'''
import logging
from logging.handlers import RotatingFileHandler

from aiservice.common.config import PROJECT_ROOT

# 日志格式: 时间 | 级别 | 线程名 | 模块:行号 | 内容
_LOG_FORMAT = '%(asctime)s | %(levelname)-7s | %(threadName)-12s | %(name)s:%(lineno)d | %(message)s'
_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

_initialized = False


def setup_logging(config) -> None:
    """初始化日志系统 (程序入口处调用一次即可)"""
    global _initialized
    if _initialized:
        return
    level_name = str(config.get('log.level', 'INFO')).upper()
    level = getattr(logging, level_name, logging.INFO)
    log_dir = PROJECT_ROOT / str(config.get('log.dir', 'logs'))
    log_dir.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    root = logging.getLogger()
    root.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    # 文件输出: 超过 max_bytes 自动轮转, 最多保留 backup_count 个历史文件
    file_handler = RotatingFileHandler(
        log_dir / str(config.get('log.file', 'server.log')),
        maxBytes=int(config.get('log.max_bytes', 10 * 1024 * 1024)),
        backupCount=int(config.get('log.backup_count', 5)),
        encoding='utf-8',
    )
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)
    _initialized = True


def get_logger(name: str) -> logging.Logger:
    """获取指定模块的 logger (自动继承根 logger 的 handler 与级别)"""
    return logging.getLogger(name)

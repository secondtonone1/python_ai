'''
全局配置管理模块
================
1. 配置与代码分离: 端口/数据库/机器人话术/限流参数全部写在 config/config.json,
   修改配置无需改代码 (企业级基本要求)
2. 单例模式: 整个进程只有一份配置 (对应课程 02_advance/16_单例模式.py)
'''
import json
from pathlib import Path

# 项目根目录 (ai_service/): 通过包结构向上推导, 与启动位置无关
PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Config:
    """配置管理器(单例)"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        # 单例: 无论 new 多少次, 都返回同一个对象 (对应课程 16_单例模式.py)
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_file: str | Path | None = None):
        if getattr(self, '_loaded', False):
            return  # 已加载过配置, 不再重复加载
        if config_file is None:
            config_file = PROJECT_ROOT / 'config' / 'config.json'
        with open(config_file, 'r', encoding='utf-8') as f:
            self._data = json.load(f)
        self._loaded = True

    @classmethod
    def instance(cls, config_file: str | Path | None = None) -> 'Config':
        """获取配置单例"""
        return cls(config_file)

    @classmethod
    def reset(cls) -> None:
        """重置单例 (仅单元测试使用)"""
        cls._instance = None

    def get(self, key: str, default=None):
        """按点号路径读取配置, 如 get('server.port') -> 8000; 取不到时返回默认值"""
        node = self._data
        for part in key.split('.'):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    def section(self, key: str) -> dict:
        """读取一个配置小节(必须是 dict), 如 section('bot')"""
        return self.get(key, {}) or {}

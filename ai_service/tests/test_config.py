'''
配置加载单元测试
================
覆盖: 点号路径读取 / 默认值 / 小节读取 / 缺失 key / 单例。
'''
import json
import os
import tempfile
import unittest

from aiservice.common.config import Config


class TestConfig(unittest.TestCase):

    def setUp(self):
        Config.reset()  # 每个用例使用独立的全新配置实例
        self._tmp = tempfile.NamedTemporaryFile(
            'w', suffix='.json', delete=False, encoding='utf-8')
        json.dump({
            'server': {'port': 9000},
            'nested': {'a': {'b': 1}},
        }, self._tmp)
        self._tmp.close()
        self.config = Config(self._tmp.name)

    def tearDown(self):
        os.unlink(self._tmp.name)
        Config.reset()

    def test_dotted_path(self):
        self.assertEqual(self.config.get('server.port'), 9000)

    def test_default_value(self):
        self.assertIsNone(self.config.get('server.host'))
        self.assertEqual(self.config.get('server.host', '0.0.0.0'), '0.0.0.0')

    def test_section(self):
        self.assertEqual(self.config.section('nested'), {'a': {'b': 1}})

    def test_deep_nested(self):
        self.assertEqual(self.config.get('nested.a.b'), 1)

    def test_missing_key(self):
        self.assertIsNone(self.config.get('not_exist'))
        self.assertEqual(self.config.get('not_exist', 'fallback'), 'fallback')

    def test_singleton(self):
        """单例: 再次 new 返回同一个对象"""
        self.assertIs(Config(), self.config)


if __name__ == '__main__':
    unittest.main()

'''
接口冒烟测试
============
用 FastAPI 自带的 TestClient 验证: 健康检查 / 统一异常响应格式 / 参数校验映射。
不依赖真实数据库 (health 与参数校验路径不碰 DB)。
'''
import unittest

from fastapi.testclient import TestClient

from aiservice.main import app


class TestApi(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        resp = self.client.get('/api/health')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['code'], 200)

    def test_validation_error_unified_format(self):
        """Pydantic 校验失败: 返回统一 {code, message} 格式 (而不是默认 422 格式)"""
        resp = self.client.post('/api/message/1/rate', json={'rating': 99})
        self.assertEqual(resp.status_code, 400)
        body = resp.json()
        self.assertEqual(body['code'], 400)
        self.assertIn('rating', body['message'])

    def test_index_page(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('html', resp.headers.get('content-type', ''))

    def test_staff_page(self):
        resp = self.client.get('/staff')
        self.assertEqual(resp.status_code, 200)

    def test_ws_ping_pong(self):
        """WebSocket 心跳: ping -> pong (不依赖数据库)"""
        with self.client.websocket_connect('/ws/chat/1') as websocket:
            websocket.send_json({'type': 'ping'})
            data = websocket.receive_json()
            self.assertEqual(data['type'], 'pong')


if __name__ == '__main__':
    unittest.main()

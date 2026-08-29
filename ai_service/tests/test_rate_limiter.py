'''
滑动窗口限流器单元测试
======================
通过注入模拟时间(now 参数)精确控制窗口滑动, 不依赖真实等待。
'''
import unittest

from aiservice.service.rate_limiter import RateLimiter


class TestRateLimiter(unittest.TestCase):

    def test_allow_within_limit(self):
        """窗口内未超限: 全部放行"""
        limiter = RateLimiter(max_requests=3, window_seconds=60)
        for i in range(3):
            allowed, _ = limiter.allow('key1', now=100.0 + i)
            self.assertTrue(allowed)

    def test_deny_over_limit(self):
        """超过上限: 拒绝并给出建议等待秒数"""
        limiter = RateLimiter(max_requests=2, window_seconds=60)
        self.assertTrue(limiter.allow('key1', now=100)[0])
        self.assertTrue(limiter.allow('key1', now=101)[0])
        allowed, retry_after = limiter.allow('key1', now=102)
        self.assertFalse(allowed)
        self.assertGreater(retry_after, 0)
        self.assertLessEqual(retry_after, 60)

    def test_window_slides(self):
        """窗口滑动: 过期请求不再计入, 可再次放行"""
        limiter = RateLimiter(max_requests=2, window_seconds=60)
        limiter.allow('key1', now=100)
        limiter.allow('key1', now=101)
        self.assertFalse(limiter.allow('key1', now=120)[0])
        # 第一个请求(now=100)已滑出窗口 -> 放行
        self.assertTrue(limiter.allow('key1', now=161)[0])

    def test_keys_are_independent(self):
        """不同 key 之间互不影响"""
        limiter = RateLimiter(max_requests=1, window_seconds=60)
        self.assertTrue(limiter.allow('a', now=100)[0])
        self.assertTrue(limiter.allow('b', now=100)[0])
        self.assertFalse(limiter.allow('a', now=101)[0])

    def test_cleanup_removes_stale_keys(self):
        """清理长时间无访问的 key"""
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        limiter.allow('stale', now=100)
        limiter.allow('fresh', now=500)
        limiter.cleanup(now=500)
        # stale 已被清理, 从零计数 -> 放行; fresh 计数保留
        self.assertTrue(limiter.allow('stale', now=500)[0])
        self.assertTrue(limiter.allow('fresh', now=501)[0])
        # fresh 累计 2 次, 窗口内再发 3 次达到上限
        for i in range(2, 5):
            self.assertTrue(limiter.allow('fresh', now=500 + i)[0])
        self.assertFalse(limiter.allow('fresh', now=506)[0])


if __name__ == '__main__':
    unittest.main()

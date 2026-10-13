'''
大模型客户端 (OpenAI 兼容 chat/completions)
==========================================
为"咨询师 AI 检索润色"提供真实大模型调用能力 (本阶段可选能力):
- 通过 config.json 的 polisher.llm 配置 base_url / model / api_key;
- api_key 优先取配置里的 api_key 字段, 为空时回退到环境变量 (api_key_env, 默认 DEEPSEEK_API_KEY);
- 不配置 key 时抛 LmNotConfigured, 上层 (ReplyPolisher) 会回退到内置规则润色,
  保证演示不中断 —— 对应课程"快速失败 + 优雅降级"的思想。

后续接入不同模型时, 只需替换 base_url/model, 无需改业务代码。
'''
import json
import os
import urllib.request
import urllib.error

from aiservice.common.config import Config
from aiservice.common.logger import get_logger


class LmNotConfigured(RuntimeError):
    """未配置大模型 API Key"""


class LlmClient:
    """极简 OpenAI 兼容 chat/completions 客户端 (仅依赖标准库)"""

    def __init__(self):
        self._config = Config.instance()
        self._logger = get_logger(__name__)
        llm = dict(self._config.get('polisher.llm', {}) or {})
        self._base_url = str(llm.get('base_url', 'https://api.deepseek.com')).rstrip('/')
        self._model = str(llm.get('model', 'deepseek-chat'))
        self._temperature = float(llm.get('temperature', 0.7))
        self._max_tokens = int(llm.get('max_tokens', 500))
        self._timeout = int(llm.get('timeout_seconds', 60))
        api_key = str(llm.get('api_key', '') or '')
        if not api_key:
            env_name = str(llm.get('api_key_env', 'DEEPSEEK_API_KEY'))
            api_key = os.environ.get(env_name, '')
        self._api_key = api_key.strip()

    @property
    def configured(self) -> bool:
        return bool(self._api_key)

    def chat(self, system: str, user: str) -> str:
        """调用模型补全一条对话, 返回助手文本"""
        if not self.configured:
            raise LmNotConfigured('未配置大模型 API Key (config: polisher.llm.api_key 或环境变量)')
        payload = {
            'model': self._model,
            'messages': [
                {'role': 'system', 'content': system},
                {'role': 'user', 'content': user},
            ],
            'temperature': self._temperature,
            'max_tokens': self._max_tokens,
            'stream': False,
        }
        url = f'{self._base_url}/chat/completions'
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json',
                     'Authorization': f'Bearer {self._api_key}'},
            method='POST',
        )
        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as resp:
                body = json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            self._logger.error(f'大模型接口 HTTP {e.code}: {e.read()[:300]!r}')
            raise RuntimeError(f'大模型接口返回 HTTP {e.code}') from e
        except Exception as e:
            self._logger.error(f'大模型接口调用失败: {e}')
            raise RuntimeError(f'大模型接口调用失败: {e}') from e
        try:
            return body['choices'][0]['message']['content'].strip()
        except (KeyError, IndexError, TypeError) as e:
            self._logger.error(f'大模型返回结构异常: {body}')
            raise RuntimeError('大模型返回结构异常') from e

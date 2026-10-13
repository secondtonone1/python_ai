'''
咨询师 "AI 检索润色" 引擎 (ReplyPolisher)
========================================
场景: 咨询师接入会话后, 点击"AI 检索润色" -> 服务端根据来访者最近一条消息
检索知识库 + 润色成一段可以直接发给来访者的回复草稿。

与 BotEngine 一样是可插拔设计 (对应课程 11/12 多态 + docs/02 引擎抽象思路):
    ReplyPolisher (抽象)
        ├── RulePolisher   内置: 知识库检索 + 共情语气模板润色 (零依赖, 默认可用)
        └── LLMPolisher    真实大模型: 检索要点 + 提示词交给 LLM 生成 (需配置 API Key)

装配策略 (config.polisher.mode):
    auto  -> 配了 Key 用 LLM, 没配 Key 自动降级规则版 (演示不中断)
    llm   -> 强制大模型 (未配置时报错)
    rule  -> 强制内置规则版
'''
from abc import ABC, abstractmethod
from dataclasses import dataclass

from aiservice.common.config import Config
from aiservice.common.logger import get_logger
from aiservice.service.llm_client import LlmClient, LmNotConfigured
from aiservice.service.bot_engine import RuleEngine


@dataclass
class PolishedReply:
    """润色结果"""
    draft: str                 # 可直接发送的回复草稿
    engine: str                # 'llm' | 'rule'
    knowledge_id: int | None = None   # 检索命中的知识条目 id (无命中为 None)
    note: str = ''             # 附加说明 (如降级提示)


class ReplyPolisher(ABC):
    """润色引擎抽象基类"""

    @abstractmethod
    def polish(self, question: str, knowledge: list[dict],
               recent: list[dict] | None = None, brief: str | None = None) -> PolishedReply:
        """生成/润色咨询师回复草稿
        :param question: 来访者最近一条消息 (需要回应的核心)
        :param knowledge: 知识库条目列表 (外部传入, 引擎不碰数据库)
        :param recent: 可选, 会话最近几条消息, 供上下文参考
        :param brief: 可选, 咨询师已写好的草稿。传入 -> "润色这段草稿";
                      为空 -> "根据来访者消息 + 知识库生成新草稿"
        """


# ---------------- 规则版 (零依赖兜底) ----------------

class RulePolisher(ReplyPolisher):
    """内置润色: 知识库检索最佳匹配 + 共情语气模板"""

    _OPENER = '我听到你最近被这件事困扰着，先谢谢你愿意把感受讲出来。'
    _CLOSER = '如果需要的话，也可以预约一次咨询，我们一起把这件事看得更清楚些。'
    _NO_HIT = ('我感受到你现在有一些困扰，这很值得被认真对待。'
               '为了能给你更有针对性的回应，可以和我说说具体发生了什么吗？')

    def __init__(self):
        self._logger = get_logger(__name__)

    def polish(self, question: str, knowledge: list[dict],
               recent: list[dict] | None = None, brief: str | None = None) -> PolishedReply:
        # 内置规则版不具备"改写自然语言"能力: 润色已有草稿时保留原文并如实说明
        if brief:
            return PolishedReply(draft=brief.strip(), engine='rule',
                                 note='内置润色仅支持生成模式, 已保留您的草稿; 配置大模型后支持改写')
        entry = self._best_knowledge(question, knowledge)
        if entry is None:
            return PolishedReply(draft=self._NO_HIT, engine='rule', note='未命中知识库, 已生成引导式回复')
        draft = f'{self._OPENER}\n\n{entry["answer"]}\n\n{self._CLOSER}'
        return PolishedReply(draft=draft, engine='rule',
                             knowledge_id=entry['id'],
                             note=f'命中知识库: {entry["question"]}')

    @staticmethod
    def _best_knowledge(question: str, knowledge: list[dict]) -> dict | None:
        """复用规则引擎的匹配打分, 取最高分条目 (并列取第一条)"""
        scored = []
        for entry in knowledge:
            score = RuleEngine._match_score(question, entry)
            if score > 0:
                scored.append((score, entry))
        if not scored:
            return None
        scored.sort(key=lambda item: -item[0])
        return scored[0][1]


# ---------------- 真实大模型版 ----------------

class LLMPolisher(ReplyPolisher):
    """把"检索要点 + 共情提示词"交给真实大模型生成润色稿"""

    def __init__(self, client: LlmClient, system_prompt: str):
        self._client = client
        self._system_prompt = system_prompt
        self._logger = get_logger(__name__)

    def polish(self, question: str, knowledge: list[dict],
               recent: list[dict] | None = None, brief: str | None = None) -> PolishedReply:
        if not self._client.configured:
            raise LmNotConfigured('未配置大模型 API Key')
        entry = RulePolisher._best_knowledge(question, knowledge)
        hit = ''
        if entry:
            hit = f'题目:{entry["question"]}\n要点:{entry["answer"]}'
        if brief:
            # 模式B: 润色咨询师已写好的草稿 (保持原意, 语气更专业/共情)
            instruction = ('任务: 润色下面这段"咨询师草稿", 保持原意不变, '
                           '让语气更温和共情、表达更专业得体, 可适度精简; '
                           '直接输出润色后的正文, 不要解释。\n\n咨询师草稿:\n'
                           + brief.strip())
        else:
            # 模式A: 根据来访者消息 + 知识库生成新草稿
            instruction = ('任务: 以咨询师口吻为来访者最近一条消息起草回复。'
                           '先接住情绪, 再结合知识库要点给出 1-2 条可操作建议。\n\n'
                           f'来访者最近一条消息:\n{question}')
        user = f'{instruction}\n\n知识库可参考要点:\n{hit or "（无直接命中，请基于共情与一般性心理支持知识回应）"}'
        draft = self._client.chat(self._system_prompt, user)
        mode_note = '已润色您的草稿' if brief else '已生成回答草稿'
        return PolishedReply(draft=draft, engine='llm',
                             knowledge_id=entry['id'] if entry else None,
                             note=f'{mode_note}; ' + (f'命中知识库: {entry["question"]}' if entry else '未命中知识库'))


# ---------------- 装配 ----------------

def get_polisher() -> ReplyPolisher:
    """按 config.polisher.mode 返回润色引擎 (auto: 有 Key 用 LLM, 否则规则版)"""
    config = Config.instance()
    mode = str(config.get('polisher.mode', 'auto')).lower()
    client = LlmClient()
    system_prompt = str(config.get('polisher.system_prompt', ''))

    if mode == 'llm':
        if not client.configured:
            raise LmNotConfigured('polisher.mode=llm 但未配置 API Key')
        return LLMPolisher(client, system_prompt)
    if mode == 'rule':
        return RulePolisher()
    # auto
    return LLMPolisher(client, system_prompt) if client.configured else RulePolisher()

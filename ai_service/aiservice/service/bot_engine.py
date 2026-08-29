'''
AI 客服引擎 (BotEngine)
========================
这是整个项目最重要的设计: 把"AI 能力"抽象成可插拔的引擎。

    BotEngine (抽象基类)
        ├── RuleEngine   本阶段: 知识库关键词规则引擎
        └── LLMEngine    后续阶段: 接入真实大模型 (LangChain/LangGraph)

上层业务(chat_service)只依赖 BotEngine 接口, 换引擎时业务代码零改动
—— 这就是面向对象"多态"在企业架构中的用法 (对应课程 11/12 多态)。
'''
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from aiservice.common.constants import MessageSource


@dataclass
class BotReply:
    """引擎一次回答的结果"""
    answer: str                                  # 回答文本
    source: str                                  # 回答来源 (见 MessageSource)
    knowledge_id: int | None = None              # 命中的知识条目 id (命中时用于统计)
    pending: list[dict] | None = None            # 追问选项 (让用户选序号的多轮状态)
    need_human: bool = False                     # 是否需要转人工


class BotEngine(ABC):
    """AI 客服引擎抽象基类: 所有引擎实现必须提供 reply 方法"""

    @abstractmethod
    def reply(self, question: str, knowledge: list[dict],
              pending: list[dict] | None = None) -> BotReply:
        """根据用户问题生成回答
        :param question: 用户输入
        :param knowledge: 知识库条目列表 (数据由外部传入, 引擎不碰数据库 -> 易于单元测试)
        :param pending: 上一轮的追问选项 (多轮上下文, 无则为 None)
        """


class RuleEngine(BotEngine):
    """知识库规则引擎 (本阶段实现)

    匹配算法:
    1. 若上一轮存在"追问选项"(多条答案并列), 优先解析用户回复的序号
    2. 关键词匹配打分: 每条知识命中一个关键词 +1 分, 命中标准问题全文 +2 分
    3. 唯一最高分 -> 直接返回答案; 多条并列最高分 -> 返回追问让用户选择
    4. 无任何命中 -> 返回转人工话术
    """

    def __init__(self, fallback_message: str, pending_prompt: str):
        self._fallback_message = fallback_message
        self._pending_prompt = pending_prompt

    def reply(self, question: str, knowledge: list[dict],
              pending: list[dict] | None = None) -> BotReply:
        question = question.strip()

        # ---- 第一优先: 上一轮的追问选择 ----
        if pending:
            idx = self._parse_choice(question)
            if idx is not None and 0 <= idx < len(pending):
                entry = pending[idx]
                return BotReply(entry['answer'], MessageSource.KNOWLEDGE, entry['id'])

        # ---- 第二优先: 关键词匹配打分 ----
        scored = []
        for entry in knowledge:
            score = self._match_score(question, entry)
            if score > 0:
                scored.append((score, entry))
        scored.sort(key=lambda item: -item[0])

        if not scored:
            # 无任何命中 -> 转人工
            return BotReply(self._fallback_message, MessageSource.FALLBACK, need_human=True)

        top_score = scored[0][0]
        tops = [entry for score, entry in scored if score == top_score]

        if len(tops) == 1:
            entry = tops[0]
            return BotReply(entry['answer'], MessageSource.KNOWLEDGE, entry['id'])

        # 多条并列最高分 -> 追问澄清 (多轮对话上下文)
        options = '\n'.join(f'{i + 1}. {entry["question"]}' for i, entry in enumerate(tops))
        return BotReply(
            self._pending_prompt.format(options=options),
            MessageSource.PENDING,
            pending=tops,
        )

    @staticmethod
    def _match_score(question: str, entry: dict) -> int:
        """计算单条知识与用户问题的匹配得分"""
        score = 0
        # 关键词: 支持中文/英文逗号分隔, 命中一个 +1
        for keyword in entry['keywords'].replace('，', ',').split(','):
            keyword = keyword.strip()
            if keyword and keyword in question:
                score += 1
        # 标准问题完整出现: +2 (权重大于单个关键词)
        if entry['question'] in question:
            score += 2
        return score

    @staticmethod
    def _parse_choice(question: str) -> int | None:
        """从用户回复中解析序号: 支持 '1'、'第2个'、'一' 等写法, 返回下标(从0开始)"""
        text = question.strip()
        chinese_digits = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
                          '六': 6, '七': 7, '八': 8, '九': 9}
        if text in chinese_digits:
            return chinese_digits[text] - 1
        match = re.search(r'\d+', text)
        if match:
            number = int(match.group())
            if number >= 1:
                return number - 1
        return None


def split_answer(answer: str, max_len: int = 8) -> list[str]:
    """把回答切分成流式输出的分片 (模拟大模型逐 token 输出)

    真实大模型接口会以 token 为单位流式返回文本,
    本项目用"按标点分句、长句再按长度切块"来模拟同样的效果,
    后续接入真实 LLM 时, 这里替换为对接模型的流式接口即可。
    """
    parts = re.split(r'(?<=[。！？；\n])', answer)
    chunks = []
    for part in parts:
        if not part:
            continue
        while len(part) > max_len:
            chunks.append(part[:max_len])
            part = part[max_len:]
        chunks.append(part)
    return chunks or [answer]

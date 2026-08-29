'''
规则引擎单元测试 (AI 核心逻辑)
================================
覆盖: 唯一命中 / 多条并列追问 / 序号选择 / 中文数字选择 / 未命中转人工 / 流式分片。
RuleEngine 不依赖数据库, 知识数据直接传入 -> 纯逻辑测试, 速度快且稳定。
'''
import unittest

from aiservice.common.constants import MessageSource
from aiservice.service.bot_engine import RuleEngine, split_answer

FALLBACK = '抱歉, 转人工'
PENDING_PROMPT = '您可能想问: \n{options}\n请回复序号'

KNOWLEDGE = [
    {'id': 1, 'category': '课程', 'question': '课程怎么收费',
     'keywords': '学费,价格,多少钱', 'answer': '学费 6980 元。'},
    {'id': 2, 'category': '课程', 'question': '什么时候开班',
     'keywords': '开班,时间', 'answer': '每月 1 号和 15 号开班。'},
    {'id': 3, 'category': '其他', 'question': '怎么退款',
     'keywords': '退款,退费', 'answer': '开课前可全额退款。'},
]


def make_engine() -> RuleEngine:
    return RuleEngine(FALLBACK, PENDING_PROMPT)


class TestRuleEngine(unittest.TestCase):

    def test_unique_hit(self):
        """唯一命中: 返回对应答案并标记知识库来源"""
        reply = make_engine().reply('你们的学费多少钱', KNOWLEDGE)
        self.assertEqual(reply.answer, '学费 6980 元。')
        self.assertEqual(reply.source, MessageSource.KNOWLEDGE)
        self.assertEqual(reply.knowledge_id, 1)
        self.assertFalse(reply.need_human)

    def test_question_full_match_scores_higher(self):
        """标准问题全文出现时权重更高, 应优先命中"""
        reply = make_engine().reply('请问课程怎么收费', KNOWLEDGE)
        self.assertEqual(reply.knowledge_id, 1)

    def test_no_hit_falls_back(self):
        """无任何命中: 返回转人工话术"""
        reply = make_engine().reply('今天天气怎么样', KNOWLEDGE)
        self.assertEqual(reply.answer, FALLBACK)
        self.assertEqual(reply.source, MessageSource.FALLBACK)
        self.assertTrue(reply.need_human)

    def test_tie_returns_pending(self):
        """多条并列最高分: 返回追问选项, 等待用户选择"""
        knowledge = KNOWLEDGE + [{
            'id': 4, 'category': '课程', 'question': '课程价格多少',
            'keywords': '价格', 'answer': '详情请咨询。',
        }]
        reply = make_engine().reply('价格', knowledge)  # 条目1和4各命中"价格"
        self.assertEqual(reply.source, MessageSource.PENDING)
        self.assertIsNotNone(reply.pending)
        self.assertEqual(len(reply.pending), 2)

    def test_pending_choice_by_number(self):
        """追问状态: 回复数字序号命中对应条目"""
        engine = make_engine()
        knowledge = KNOWLEDGE + [{
            'id': 4, 'category': '课程', 'question': '课程价格多少',
            'keywords': '价格', 'answer': '详情请咨询。',
        }]
        reply = engine.reply('价格', knowledge)
        # 并列项按知识库顺序排列: [条目1(价格), 条目4(价格)], 序号2 -> 条目4
        chosen = engine.reply('2', knowledge, reply.pending)
        self.assertEqual(chosen.knowledge_id, 4)
        self.assertEqual(chosen.answer, '详情请咨询。')

    def test_pending_choice_by_chinese_digit(self):
        """追问状态: 回复中文数字"""
        engine = make_engine()
        knowledge = KNOWLEDGE + [{
            'id': 4, 'category': '课程', 'question': '课程价格多少',
            'keywords': '价格', 'answer': '详情请咨询。',
        }]
        reply = engine.reply('价格', knowledge)
        chosen = engine.reply('一', knowledge, reply.pending)
        self.assertEqual(chosen.knowledge_id, 1)

    def test_pending_invalid_choice_falls_through(self):
        """追问状态下回复了无效内容: 走普通匹配"""
        engine = make_engine()
        knowledge = KNOWLEDGE + [{
            'id': 4, 'category': '课程', 'question': '课程价格多少',
            'keywords': '价格', 'answer': '详情请咨询。',
        }]
        reply = engine.reply('价格', knowledge)
        chosen = engine.reply('什么时候开班', knowledge, reply.pending)
        self.assertEqual(chosen.knowledge_id, 2)


class TestSplitAnswer(unittest.TestCase):

    def test_split_by_punctuation(self):
        """按标点分句"""
        chunks = split_answer('第一句。第二句！', 8)
        self.assertEqual(chunks, ['第一句。', '第二句！'])

    def test_split_long_sentence(self):
        """长句按长度切块"""
        chunks = split_answer('一二三四五六七八九十', 4)
        self.assertEqual(chunks, ['一二三四', '五六七八', '九十'])

    def test_empty_answer(self):
        self.assertEqual(split_answer(''), [''])


if __name__ == '__main__':
    unittest.main()

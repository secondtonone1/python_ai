'''
AI 润色引擎 (ReplyPolisher) 单元测试
====================================
覆盖内置规则润色: 命中知识库 / 未命中引导 / 不依赖网络与 API Key。
'''
import unittest

from aiservice.service.reply_polisher import RulePolisher

KNOWLEDGE = [
    {'id': 1, 'category': '情绪困扰', 'question': '总是很焦虑、静不下来怎么办',
     'keywords': '焦虑,紧张,心慌', 'answer': '试试 4-7-8 呼吸法。'},
    {'id': 2, 'category': '睡眠困扰', 'question': '晚上睡不着、失眠怎么办',
     'keywords': '失眠,睡不着', 'answer': '睡前 1 小时关掉短视频。'},
]


class TestRulePolisher(unittest.TestCase):

    def test_hit_knowledge(self):
        """命中知识库: 草稿包含检索到的要点, 并标记命中条目"""
        result = RulePolisher().polish('最近总是很焦虑', KNOWLEDGE)
        self.assertEqual(result.engine, 'rule')
        self.assertEqual(result.knowledge_id, 1)
        self.assertIn('4-7-8', result.draft)
        self.assertGreater(len(result.draft), 20)

    def test_no_hit_guides(self):
        """未命中: 返回共情引导式草稿, 不带 knowledge_id"""
        result = RulePolisher().polish('我家的猫丢了很伤心', KNOWLEDGE)
        self.assertEqual(result.engine, 'rule')
        self.assertIsNone(result.knowledge_id)
        self.assertGreater(len(result.draft), 20)

    def test_tie_takes_first(self):
        """并列命中: 取列表第一条作为要点"""
        knowledge = KNOWLEDGE + [{'id': 3, 'category': '测试', 'question': '焦虑测试',
                                  'keywords': '焦虑', 'answer': '并列项。'}]
        result = RulePolisher().polish('焦虑', knowledge)
        self.assertEqual(result.knowledge_id, 1)

    def test_brief_keeps_original(self):
        """润色已有草稿: 规则版不具备改写能力, 保留原文并说明"""
        brief = '别担心，会好的。'
        result = RulePolisher().polish('最近总是很焦虑', KNOWLEDGE, brief=brief)
        self.assertEqual(result.draft, brief)
        self.assertIn('保留您的草稿', result.note)


if __name__ == '__main__':
    unittest.main()

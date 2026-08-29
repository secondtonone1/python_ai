# -*- coding: utf-8 -*-
"""
端到端验收测试 (对应 docs/01_需求文档.md 第 6 章验收标准)
覆盖: 健康检查 / 创建会话 / WS流式对话 / 追问澄清 / 转人工 /
      满意度评价 / 客服登录 / 会话列表 / 接管 / 回复推送 / 统计 /
      知识库增删 / 限流429 / 未认证401
"""
import asyncio
import json
import sys

import httpx
import websockets

BASE = 'http://127.0.0.1:8000'
WS = 'ws://127.0.0.1:8000'
PASS, FAIL = [], []


def check(name: str, cond: bool, detail: str = ''):
    (PASS if cond else FAIL).append(name)
    print(f'  [{"PASS" if cond else "FAIL"}] {name}  {detail}')


async def recv_until(ws, stop_types: set, timeout: float = 30):
    """持续接收直到收到 stop_types 中的帧, 返回收到的所有帧"""
    frames = []
    while True:
        raw = await asyncio.wait_for(ws.recv(), timeout)
        msg = json.loads(raw)
        frames.append(msg)
        if msg['type'] in stop_types:
            return frames


async def main():
    async with httpx.AsyncClient(base_url=BASE, timeout=15) as c:

        # 1. 健康检查
        r = await c.get('/api/health')
        check('健康检查', r.status_code == 200 and r.json()['code'] == 200, str(r.json()))

        # 2. 创建会话
        r = await c.post('/api/session', json={'visitor_name': '验收测试访客'})
        body = r.json()
        check('创建会话', body['code'] == 200 and body['data']['status'] == 'bot', str(body))
        sid = body['data']['id']

        # 3. 客服未认证 -> 401
        r = await c.get('/api/staff/sessions')
        check('未认证401', r.status_code == 401 and r.json()['code'] == 401, str(r.json()))

        # 4. 客服登录
        r = await c.post('/api/staff/login', json={'username': 'admin', 'password': '123456'})
        staff = r.json()['data']
        headers = {'X-Staff-Id': str(staff['id'])}
        check('客服登录', r.json()['code'] == 200 and staff['username'] == 'admin', str(staff))

        # 5. WebSocket 流式对话 + 满意度评价
        async with websockets.connect(f'{WS}/ws/chat/{sid}') as ws:
            await ws.send(json.dumps({'type': 'chat', 'content': '学费多少钱'}))
            frames = await recv_until(ws, {'message_end'})
            chunks = ''.join(f['delta'] for f in frames if f['type'] == 'chunk')
            end = next(f for f in frames if f['type'] == 'message_end')
            check('流式对话-唯一命中', end['message']['source'] == 'knowledge',
                  f'答案={end["message"]["content"][:30]}... 分片数={len(chunks)}')
            check('流式分片还原', chunks == end['message']['content'],
                  f'{len(chunks)} 分片')
            mid = end['message']['id']

            r = await c.post(f'/api/message/{mid}/rate', json={'rating': 1})
            check('满意度评价', r.json()['code'] == 200, str(r.json()))

            # 6. 追问澄清: 先新增一条与"价格"并列的知识 -> 触发追问
            r = await c.post('/api/staff/knowledge', headers=headers, json={
                'category': '测试', 'question': '价格怎么谈',
                'keywords': '价格', 'answer': '价格可面谈。'})
            kid = r.json()['data']['knowledge_id']
            check('知识库新增', r.json()['code'] == 200, str(r.json()))

            await ws.send(json.dumps({'type': 'chat', 'content': '价格'}))
            frames = await recv_until(ws, {'message_end', 'session_status'})
            ends = [f for f in frames if f['type'] == 'message_end']
            if ends:
                check('并列追问', ends[-1]['message']['source'] == 'pending',
                      f'内容={ends[-1]["message"]["content"][:40]}...')
                # 7. 回复序号 1 选择第一个候选
                await ws.send(json.dumps({'type': 'chat', 'content': '1'}))
                frames = await recv_until(ws, {'message_end'})
                chosen = next(f for f in frames if f['type'] == 'message_end')
                check('序号选择答案', chosen['message']['source'] == 'knowledge',
                      f'答案={chosen["message"]["content"][:30]}')
            else:
                check('并列追问', False, '未触发追问')

            r = await c.delete(f'/api/staff/knowledge/{kid}', headers=headers)
            check('知识库删除', r.json()['code'] == 200, str(r.json()))

            # 8. 未命中 -> 转人工 (等待人工): 需同时收到 message_end 与 session_status
            await ws.send(json.dumps({'type': 'chat', 'content': '今天天气怎么样'}))
            seen_end, seen_status = False, None
            for _ in range(200):  # 轮询接收直到两种帧都到齐
                raw = await asyncio.wait_for(ws.recv(), 15)
                msg = json.loads(raw)
                if msg['type'] == 'message_end':
                    seen_end = True
                if msg['type'] == 'session_status':
                    seen_status = msg['status']
                if seen_end and seen_status:
                    break
            check('未命中转人工', seen_end and seen_status == 'waiting_human',
                  f'end={seen_end} status={seen_status}')

            # 9. 人工回复实时推送 (WS 保持连接)
            r = await c.get('/api/staff/sessions', params={'status': 'waiting_human'}, headers=headers)
            waiting = [s for s in r.json()['data'] if s['id'] == sid]
            check('工作台看到等待人工会话', len(waiting) == 1, str(r.json()['data'][:1]))

            r = await c.post(f'/api/staff/sessions/{sid}/takeover', headers=headers)
            check('人工接管', r.json()['code'] == 200, str(r.json()))

            r = await c.post(f'/api/staff/sessions/{sid}/reply', headers=headers,
                             json={'content': '您好，已为您转人工，请问有什么可以帮您？'})
            check('客服回复', r.json()['code'] == 200, str(r.json()))

            frames = await recv_until(ws, {'staff_reply'})
            push = next(f for f in frames if f['type'] == 'staff_reply')
            check('访客实时收到客服消息', push['message']['role'] == 'staff',
                  f'内容={push["message"]["content"][:30]}')

            # 10. 会话历史 (4次对话: user+bot; 未命中那次 bot 也有 fallback 消息; + staff 回复)
            r = await c.get(f'/api/session/{sid}/history')
            roles = [m['role'] for m in r.json()['data']]
            check('会话历史', roles == ['user', 'bot', 'user', 'bot', 'user', 'bot',
                                         'user', 'bot', 'staff'],
                  f'共{len(roles)}条: {roles}')

            # 11. 限流: 连续发 21 条 -> 第 21 条 429
            for i in range(21):
                await ws.send(json.dumps({'type': 'chat', 'content': f'测试消息{i}'}))
            got_429 = False
            for _ in range(60):
                try:
                    raw = await asyncio.wait_for(ws.recv(), 10)
                except asyncio.TimeoutError:
                    break
                msg = json.loads(raw)
                if msg['type'] == 'error' and msg['code'] == 429:
                    got_429 = True
                    break
            check('限流429', got_429, '21条内触发429')

            await ws.send(json.dumps({'type': 'ping'}))
            frames = await recv_until(ws, {'pong'})
            check('WS心跳ping/pong', any(f['type'] == 'pong' for f in frames))

        # 12. 运营统计
        r = await c.get('/api/staff/stats', headers=headers)
        stats = r.json()['data']
        check('运营统计', r.json()['code'] == 200 and 'bot_hit_rate' in stats, str(stats))

        # 13. 关闭会话
        r = await c.post(f'/api/staff/sessions/{sid}/close', headers=headers)
        check('关闭会话', r.json()['code'] == 200, str(r.json()))

    print(f'\n结果: {len(PASS)} 通过, {len(FAIL)} 失败')
    if FAIL:
        print('失败项:', FAIL)
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())

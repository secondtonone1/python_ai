# -*- coding: utf-8 -*-
"""
端到端验收测试 (对应 docs/01_需求文档.md 第 6 章验收标准)
覆盖: 健康检查 / 创建会话 / WS流式对话 / 追问澄清 / 转人工 /
      满意度评价 / 客服登录 / 会话列表 / 接管 / 回复推送 / 统计 /
      知识库增删 / 限流429 / 未认证401
"""
import asyncio
import json
import os
import sys

import httpx
import websockets

_PORT = int(os.environ.get('SMART_PORT', '8000'))
BASE = f'http://127.0.0.1:{_PORT}'
WS = f'ws://127.0.0.1:{_PORT}'
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
            await ws.send(json.dumps({'type': 'chat', 'content': '最近总是很焦虑怎么办'}))
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

            # 6. 追问澄清: 先新增一条与"压力"并列的知识 -> 触发追问
            r = await c.post('/api/staff/knowledge', headers=headers, json={
                'category': '测试', 'question': '压力很大很想躺平怎么办',
                'keywords': '压力', 'answer': '可以先允许自己休息半天，再约咨询师聊聊。'})
            kid = r.json()['data']['knowledge_id']
            check('知识库新增', r.json()['code'] == 200, str(r.json()))

            await ws.send(json.dumps({'type': 'chat', 'content': '压力'}))
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

        # 14. 客服工作台 WebSocket 推送场景 (替代轮询)
        await run_staff_ws_scenario(c)

    print(f'\n结果: {len(PASS)} 通过, {len(FAIL)} 失败')
    if FAIL:
        print('失败项:', FAIL)
        sys.exit(1)


async def _collect_staff(staff_ws, predicate, timeout: float = 8.0) -> list:
    """读取工作台推送直到出现满足 predicate 的帧, 返回读到的全部帧"""
    frames = []
    deadline = asyncio.get_running_loop().time() + timeout
    while True:
        remaining = deadline - asyncio.get_running_loop().time()
        if remaining <= 0:
            return frames
        raw = await asyncio.wait_for(staff_ws.recv(), remaining)
        msg = json.loads(raw)
        frames.append(msg)
        if predicate(msg):
            return frames


async def _drain_visitor(vis_ws, want: tuple[str, str] | None = None, timeout: float = 20.0) -> list:
    """消费访客连接直到出现匹配帧; want=(type, status), status 为 None 表示不校验;
    无 want 时读到 message_end"""
    frames = []
    while True:
        raw = await asyncio.wait_for(vis_ws.recv(), timeout)
        msg = json.loads(raw)
        frames.append(msg)
        if want:
            if msg.get('type') == want[0] and (want[1] is None or msg.get('status') == want[1]):
                return frames
        elif msg.get('type') == 'message_end':
            return frames


async def run_staff_ws_scenario(c):
    """客服工作台推送验收: 新消息/转人工/接管/回复/关闭 全部经 /ws/staff 实时到达"""
    print('--- 工作台 WebSocket 推送场景 ---')
    r = await c.post('/api/staff/login', json={'username': 'admin', 'password': '123456'})
    staff = r.json()['data']
    headers = {'X-Staff-Id': str(staff['id'])}

    # 0. 鉴权: 无效 staff_id 应被拒绝
    try:
        async with websockets.connect(f'{WS}/ws/staff?staff_id=99999') as bad_ws:
            await bad_ws.recv()
        check('工作台WS鉴权', False, '连接竟然成功')
    except Exception:
        check('工作台WS鉴权', True, '无效 id 被关闭')

    async with websockets.connect(f'{WS}/ws/staff?staff_id={staff["id"]}') as staff_ws:
        # 心跳
        await staff_ws.send(json.dumps({'type': 'ping'}))
        frames = await _collect_staff(staff_ws, lambda m: m['type'] == 'pong')
        check('工作台WS心跳', any(f['type'] == 'pong' for f in frames))

        # 1. 访客提问(知识库命中): 工作台实时收到 user 消息 + bot 消息 + 会话事件
        r = await c.post('/api/session', json={'visitor_name': '推送测试'})
        sid = r.json()['data']['id']
        async with websockets.connect(f'{WS}/ws/chat/{sid}') as vis_ws:
            await vis_ws.send(json.dumps({'type': 'chat', 'content': '最近总是很焦虑怎么办'}))
            frames = await _collect_staff(staff_ws, lambda m: m['type'] == 'staff_session')
            msgs = [f['message'] for f in frames if f['type'] == 'staff_message']
            sess = [f['session'] for f in frames if f['type'] == 'staff_session']
            check('工作台推送-命中消息', len(msgs) >= 2 and msgs[0]['role'] == 'user'
                  and msgs[1]['role'] == 'bot' and msgs[1]['source'] == 'knowledge',
                  f'共{len(msgs)}条消息')
            check('工作台推送-会话事件', sess and sess[-1]['id'] == sid, str(sess))
            await _drain_visitor(vis_ws)

            # 2. 未命中 -> 转人工: 工作台收到 waiting_human 会话事件 (列表实时出现)
            await vis_ws.send(json.dumps({'type': 'chat', 'content': '今天天气怎么样'}))
            frames = await _collect_staff(
                staff_ws, lambda m: m['type'] == 'staff_session' and m['session']['status'] == 'waiting_human')
            got = any(f['type'] == 'staff_session' and f['session']['id'] == sid
                      and f['session']['status'] == 'waiting_human' for f in frames)
            check('工作台推送-新转人工', got, str(frames[-1:]))
            await _drain_visitor(vis_ws, want=('session_status', 'waiting_human'))

            # 3. 接管: 工作台收到 human 事件, 访客收到 session_status human
            r = await c.post(f'/api/staff/sessions/{sid}/takeover', headers=headers)
            check('接管接口', r.json()['code'] == 200, str(r.json()))
            frames = await _collect_staff(
                staff_ws, lambda m: m['type'] == 'staff_session' and m['session']['status'] == 'human')
            check('工作台推送-被接管', any(f['session']['id'] == sid and f['session']['status'] == 'human'
                                         for f in frames if f['type'] == 'staff_session'))
            await _drain_visitor(vis_ws, want=('session_status', 'human'))

            # 3.5 AI 检索润色 (咨询师助手): 接入后可生成可编辑草稿
            r = await c.post(f'/api/staff/sessions/{sid}/polish', headers=headers)
            body = r.json()
            pdata = body.get('data') or {}
            check('AI润色生成草稿', body.get('code') == 200 and len(pdata.get('draft', '')) > 20
                  and pdata.get('engine') in ('llm', 'rule') and pdata.get('mode') == 'generate',
                  f"engine={pdata.get('engine')} 草稿长度={len(pdata.get('draft', ''))}")

            # 3.6 AI 润色-润色已有草稿模式 (传 content 后 mode=polish)
            r = await c.post(f'/api/staff/sessions/{sid}/polish', headers=headers,
                             json={'content': '别太担心，我会陪你一起想办法。'})
            body2 = r.json()
            pdata2 = body2.get('data') or {}
            check('AI润色-润色草稿模式', body2.get('code') == 200
                  and pdata2.get('mode') == 'polish' and len(pdata2.get('draft', '')) > 0,
                  f"mode={pdata2.get('mode')} engine={pdata2.get('engine')}")

            # 4. 客服回复: 工作台收到 staff 消息, 访客实时收到 staff_reply
            r = await c.post(f'/api/staff/sessions/{sid}/reply', headers=headers,
                             json={'content': '您好，请问有什么可以帮您？'})
            check('回复接口', r.json()['code'] == 200, str(r.json()))
            frames = await _collect_staff(
                staff_ws, lambda m: m['type'] == 'staff_message' and m['message']['role'] == 'staff')
            check('工作台推送-客服消息', any(f['message']['session_id'] == sid for f in frames
                                           if f['type'] == 'staff_message'))
            vis_frames = await _drain_visitor(vis_ws, want=('staff_reply', None), timeout=10)
            check('访客实时收到客服回复', any(f['type'] == 'staff_reply' and f['message']['session_id'] == sid
                                           for f in vis_frames))

            # 5. 访客在人工中发消息: 工作台实时收到 user 消息
            await vis_ws.send(json.dumps({'type': 'chat', 'content': '我想问下就业情况'}))
            frames = await _collect_staff(
                staff_ws, lambda m: m['type'] == 'staff_message' and m['message']['role'] == 'user')
            check('工作台推送-人工中访客消息', any(f['message']['content'] == '我想问下就业情况'
                                                 for f in frames if f['type'] == 'staff_message'))
            await _drain_visitor(vis_ws, want=('session_status', 'human'))

            # 6. 关闭: 工作台收到 closed 事件, 访客收到 session_status closed
            r = await c.post(f'/api/staff/sessions/{sid}/close', headers=headers)
            check('关闭接口', r.json()['code'] == 200, str(r.json()))
            frames = await _collect_staff(
                staff_ws, lambda m: m['type'] == 'staff_session' and m['session']['status'] == 'closed')
            check('工作台推送-已关闭', any(f['session']['id'] == sid and f['session']['status'] == 'closed'
                                         for f in frames if f['type'] == 'staff_session'))
            await _drain_visitor(vis_ws, want=('session_status', 'closed'))


if __name__ == '__main__':
    asyncio.run(main())

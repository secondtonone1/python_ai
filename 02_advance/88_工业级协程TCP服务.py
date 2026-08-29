import struct
import asyncio
from asyncio import Queue

# 全局业务消息队列,IO协程产生消息，逻辑协程消费消息
MSG_QUEUE = Queue(maxsize=1000)

class TLVProtocol(object):
    # T = 2字节, L = 2字节, 头部总共4字节
    HEADER_LEN = 4

    @classmethod
    def encode(cls, msg_type:int, body: str) -> bytes:
        '''
         TLV消息打包：对外发送完整数据包
        :param msg_type: 消息ID(T)
        :param body: 业务消息内容(V)
        :return: 二进制TLV数据包
        '''
        body_bytes = body.encode('utf-8')
        body_len = len(body_bytes)
        # 网络字节序打包: 2字节消息类型+ 2字节的消息长度
        header = struct.pack('>HH', msg_type, body_len)
        return header + body_bytes

    @classmethod
    def decode(cls,buffer:bytes) ->tuple[list[dict], bytes]:
        """
            TLV消息解包：处理缓冲区数据，解析完整消息，返回未用完的半包数据
            :param buffer: 累计接收的缓冲区原始字节
            :return: 完整消息列表、剩余半包数据
            """
        messages = []
        # 循环解析，支持依次解析多条数据 + 半包残留数据
        while len(buffer) >= cls.HEADER_LEN:
            # 解析包头，获取消息整体长度
            msg_type, body_len = struct.unpack('>HH', buffer[:cls.HEADER_LEN])
            # 总共包的长度
            total_pkg_len = cls.HEADER_LEN + body_len
            # 如果数据不完整则直接退出，保留当前所有数据等待下次接受
            if len(buffer) < total_pkg_len:
                break
            # 截取完整的消息体
            body_data = buffer[cls.HEADER_LEN:total_pkg_len].decode('utf-8')
            messages.append(
                {
                    'msg_type': msg_type,
                    'body': body_data,
                    'body_len': body_len,
                }
            )

            # 截断已经解析的数据，保留剩余字节继续解析
            buffer = buffer[total_pkg_len:]

        return messages, buffer

from typing import Dict
# 客户端连接池, 保存所有在线客户端的读写对象
CLIENT_POOL:Dict[str, asyncio.StreamWriter] = dict()

async def client_logic_worker():
    '''
        全局逻辑处理协程（独立后台线程）
        专门消费消息队列，执行业务逻辑，不阻塞网络IO
    :return:
    '''
    print('业务逻辑处理协程启动成功')
    while True:
        # 阻塞获取队列消息
        msg_info = await MSG_QUEUE.get()
        msg_type = msg_info['msg_type']
        msg_body = msg_info['body']
        client_addr = msg_info['client_addr']
        print(f'客户端: {client_addr}, 消息类型: {msg_type}, 内容: {msg_body}')
        if msg_type == 1:
            resp_body = f'[聊天回执] 已收到消息: {msg_body}'
        elif msg_type == 2:
            resp_body = f'[心跳回执] 心跳检测正常'
        else:
            resp_body = f'[未知指令] 暂不支持该类消息{msg_type}'

        # 封装响应消息，交给发送协程
        if client_addr in CLIENT_POOL:
            resp_pkg = TLVProtocol.encode(msg_type, resp_body)
            writer = CLIENT_POOL[client_addr]
            writer.write(resp_pkg)
            await writer.drain()

        # 标记队列任务完成
        MSG_QUEUE.task_done()

async def client_handle(reader, writer):
    client_addr = f"{writer.get_extra_info('peername')}"
    CLIENT_POOL[client_addr] = writer
    print(f'新客户端接入: {client_addr}, 当前在线: {len(CLIENT_POOL)}')

    # 客户端私有缓冲区,永久保存半包数据，将来用来调用TLVProtocol解析
    recv_buffer = b''
    try:
        while True:
            # 异步接受数据 ，单次接受4096字节
            recv_data = await reader.read(4096)
            # 对端关闭
            if not recv_data:
                break
            # 累加消息放入缓冲区
            recv_buffer += recv_data
            # TLV解析
            full_msgs , recv_buffer = TLVProtocol.decode(recv_buffer)
            # 完整消息全部投入逻辑队列中，交由后台协程处理
            for msg in full_msgs:
                msg['client_addr'] = client_addr
                await MSG_QUEUE.put(msg)

    except Exception as e:
        print(f'客户端{client_addr}连接异常: {e}')
    finally:
        # 断开连接
        del CLIENT_POOL[client_addr]
        writer.close()
        await writer.wait_closed()
        print(f'客户端{client_addr}已经断开连接, 当前在线: {len(CLIENT_POOL)}')

async def  main():
    # 启动后台业务逻辑协程
    asyncio.create_task(client_logic_worker())
    # 启动TLV-TCP服务
    server = await asyncio.start_server(client_handle, host='0.0.0.0', port=8888)
    print(f'工业级TLV全双工TCP服务器启动成功....')
    print(f'服务器监听端口: 8888 | 协议格式T(2B) + L(2B) + V(NB)')
    await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
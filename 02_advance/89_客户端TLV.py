import asyncio
import struct

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


async def tlv_tcp_client():
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)

    # 发送不同类型TLV消息
    test_msgs = [
        (1, "你好，TCP全双工服务"),   # 1=聊天消息
        (2, "heartbeat"),            # 2=心跳包
        (1, "测试TLV协议解析")
    ]

    for msg_type, content in test_msgs:
        pkg = TLVProtocol.encode(msg_type, content)
        writer.write(pkg)
        await writer.drain()

        # 接收服务端响应
        res = await reader.read(1024)
        msgs, _ = TLVProtocol.decode(res)
        for m in msgs:
            print(f"服务端响应：{m}")

    await asyncio.sleep(2)
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(tlv_tcp_client())

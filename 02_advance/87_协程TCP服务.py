import asyncio
# 处理单个客户端连接
async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    client_addr = writer.get_extra_info('peername')
    print(f'协程客户端接入: {client_addr}')
    while True:
        # 异步非阻塞读取数据,IO等待让出CPU
        recv_data = await reader.read(1024)
        if not recv_data:
            print(f'客户端 {client_addr} 断开连接')
            break
        # 字节流转化为字符串
        msg = recv_data.decode('utf-8')
        print(f'收到{client_addr}消息: {msg}')
        # 异步发送回复的消息
        writer.write(f'协程服务器已经收到: {msg}'.encode('utf-8'))
        # 等待发送完成
        await writer.drain()
    # 关闭连接
    writer.close()
    # 等待关闭完成
    await writer.wait_closed()

# 定义主函数
async def main():
    # 启动异步TCP服务
    server = await asyncio.start_server(handle_client, host='0.0.0.0', port=10086)
    print('协程异步TCP高并发服务启动成功')
    # 服务器永久循环
    await server.serve_forever()

# 主函数
if __name__ == '__main__':
    asyncio.run(main())

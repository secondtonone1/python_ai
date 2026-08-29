'''
演示阻塞通信的TCP客户端
'''

import socket
# 1.创建TCP套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2.连接服务器
server_host = '127.0.0.1'
server_port = 10086
client_socket.connect((server_host, server_port))

#3. 循环读写数据
while True:
    input_msg = input('输入发送的消息(quit退出)')
    if input_msg == 'quit':
        break
    # 发送消息,参数是字节码，需要将字符串编成字节流
    client_socket.send(input_msg.encode('utf-8'))
    # 接受服务器消息,接收到的也是字节流，也需要解码
    res_data = client_socket.recv(1024).decode('utf-8')
    print(f'服务器回复内容为: {res_data}')

# 4.关闭套接字
client_socket.close()
'''
演示阻塞TCP服务器
'''

import socket
import threading
# 全局停止信号
global_stop = False

def create_bind():
    # 1.  创建TCP socket套接字(在英文中相当于插座)
    # 参1 IPV4/IPV6, AF_INET表示IPV4
    # 参2 流式SOCKET ，TCP通信协议
    # 返回值返回一个服务端用来监听的socket, 大白话大堂经理
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 开启端口复用，避免端口被前一个进程占用报错
    # 参1 表示socket的安全选项
    # 参2 表示地址复用
    # 参3 表示为True，也就是开启地址复用
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2.绑定IP和端口
    HOST = '0.0.0.0'
    PORT = 8888
    # bind接受tuple类型，绑定host和port
    server_socket.bind((HOST, PORT))

    # 3. 开启监听，最大挂起连接队列为5的相关参数，比5大很多
    server_socket.listen(5)
    print(f'TCP服务器启动成功,监听 {HOST}:{PORT}')
    return server_socket

def handle_client(conn,client_addr):
    try:
        # 5.循环读写数据
        while not global_stop:
            # 接受客户端数据(最大1024字节)
            recv_data = conn.recv(1024)
            if not recv_data:
                print(f'客户端 {client_addr} 断开连接')
                break
            # 字节解码，将字节流转换为字符串，因为TCP底层的传输是面向字节流的
            msg = recv_data.decode('utf-8')
            print(f'收到客户端消息: {msg}')
            # 回复客户端，将字符串转化为字节流发送给客户端
            rt_msg = '服务器已接受: ' + msg
            # 将字符串编码为字节流
            rt_bytes = rt_msg.encode('utf-8')
            # 回复客户端消息
            conn.send(rt_bytes)
    except Exception as e:
        print(e)
    finally:
        # 关闭客户端连接
        conn.close()

def server_loop(server_socket):
    # 4.服务器循环等待客户端连接
    while True:
        try:
            # server_socket接受连接，返回一个专门和客户端通信的socket，以及客户端的地址
            conn, client_addr = server_socket.accept()
            print(f'客户端接入: {client_addr}')
            # 创建线程，独立运行处理客户端的收发逻辑
            threading.Thread(target=handle_client, args=(conn, client_addr)).start()
        except Exception as e:
            print(e)
            break


if __name__ == '__main__':
    # 1.创建socket和绑定监听
    server_socket = create_bind()
    # 2. 循环接受连接，并且处理读写
    server_loop(server_socket)
    # 3. 主线程退出，将global_stop设置为True
    global_stop = True

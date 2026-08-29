---
title: Python进阶之网络编程
date: 2026-08-03 09:09:37
tags: [python,AI]
categories: [python,AI]
---

# 第一章 网络编程核心基础要素

网络编程的本质是**跨主机进程数据交互**，实现通信必须依赖三个核心要素：**IP地址、端口、通信协议**，三者唯一确定网络中的一个通信服务。

<img src="https://cdn.llfc.club/image-20260803092745062.png" alt="image-20260803092745062" style="zoom: 67%;" />

##  IP地址

IP地址是网络中**主机的唯一标识**，作用是定位互联网/局域网中的设备，分为两类：

- **IPv4**：32位地址，格式为`x.x.x.x`（如127\.0\.0\.1），目前主流使用

- **IPv6**：128位地址，解决IPv4地址枯竭问题，逐步普及

特殊IP说明：

- `127.0.0.1`：本地回环地址，仅本机可访问，用于本地测试
- `0.0.0.0`：监听本机所有网卡地址，允许局域网、本机所有设备访问服务

127.0.0.1 表示本机地址，只能本机的客户端访问本机服务器，大白话好比我们住在一个房间

172.16.17.14 局域网地址，在同一个局域网内所有局域网内的客户端可以访问服务器，好比我们在一个小区，只要通过3单元601就能找到我，因为在一个小区

81.68.86.146 外网地址，任何机器都可以通过外网地址访问服务器，好比我们不在一个小区，需要户口本上的住址找到我

0.0.0.0 万能地址(局域网地址+本机地址+外网地址)，任何机器可以访问我们服务器

##  端口（Port）

IP地址用于定位**设备**，端口用于定位**设备内的具体进程**。一台主机可通过端口区分多个网络服务。

端口范围：0\~65535（16位无符号整数），分类如下：

- 公认端口（0\~1023）：系统预留占用，如80\(HTTP\)、443\(HTTPS\)、22\(SSH\)，自定义服务禁止使用

- 注册端口（1024\~49151）：第三方服务自定义端口，开发首选区间

- 动态端口（49152\~65535）：客户端临时随机端口，无需手动配置

##  常用网络通信协议

协议是网络数据传输的规则约定，规定数据封装、传输、校验方式，Python网络编程核心接触协议如下：

### 传输层核心协议（编程重点）

- **TCP（传输控制协议）**：面向连接、可靠传输、有序无丢包，支持重传纠错，适用于文件传输、聊天、接口通信，游戏实时交互等绝大多数业务

- **UDP（用户数据报协议）**：无连接、不可靠、传输速度快，无握手流程，适用于直播、语音通话、

###  应用层常用协议

- HTTP/HTTPS：超文本传输协议，用于网页、接口请求

- FTP：文件传输协议，用于跨主机文件上传下载

- SMTP：邮件发送协议，用于邮件推送

##  TCP 核心连接机制：三次握手 + 四次挥手（断开回收）

TCP 是**面向连接的可靠协议**，区别于UDP无连接协议，TCP收发数据前必须建立连接、通信结束后必须安全释放连接、回收系统资源。三次握手负责**建立可靠连接**，四次挥手负责**安全断开连接、资源回收**，是TCP网络编程最底层核心原理。

### TCP 三次握手（建立连接）

<img src="https://cdn.llfc.club/image-20260803092001523.png" alt="image-20260803092001523" style="zoom: 67%;" />

**核心目的**：双向校验客户端、服务端的收发能力全部正常，确保连接可靠、无丢包、无单向故障。

**文字流程图解**：

- **第一次握手（客户端 → 服务端）**：客户端发送 SYN 连接请求报文，进入 SYN\_SENT 状态，告知服务端：客户端可正常发送数据。

- **第二次握手（服务端 → 客户端）**：服务端收到SYN，返回 SYN\+ACK 报文（同意连接\+确认收到请求），进入 SYN\_RCVD 状态，告知客户端：服务端收发能力正常。

- **第三次握手（客户端 → 服务端）**：客户端收到SYN\+ACK，返回 ACK 确认报文，双方进入 ESTABLISHED 连接成功状态，正式开启**全双工数据通信**。

**一句话总结**：互相确认收发正常，连接正式建立。

###  TCP 四次挥手（连接断开 \& 资源回收）

<img src="https://cdn.llfc.club/image-20260803092256803.png" alt="image-20260803092256803" style="zoom:67%;" />

**核心目的**：TCP是全双工通信，读写通道相互独立，无法一次性关闭，必须四次交互，保证残留数据传输完毕，避免数据丢失、socket资源泄漏。

**文字流程图解**：

- **第一次挥手（主动关闭方 → 被动方）**：主动断连端发送 FIN 报文，告知对方：本方无数据可发送，请求关闭发送通道。

- **第二次挥手（被动方 → 主动方）**：被动方返回 ACK 确认，进入**半关闭状态**：主动方不能发数据，但可以收数据，被动方可持续发送剩余数据。

- **第三次挥手（被动方 → 主动方）**：被动方数据全部发送完成，发送 FIN 报文，告知对方：本方数据发送完毕，可关闭连接。

- **第四次挥手（主动方 → 被动方）**：主动方返回 ACK 确认，等待超时确保报文送达，双方正式断开连接，系统回收端口、socket内存资源。

###  经典面试核心问题

**为什么建立连接是三次握手，断开连接需要四次挥手？**

建连时：SYN请求连接 和 ACK确认报文 可以合并为一次发送；
断连时：被动方收到FIN后，可能还有业务剩余数据需要发送，不能立刻关闭，必须先确认、再传完数据、最后关闭，因此必须四次挥手。

###  代码层对应关系

- 三次握手：底层自动完成，对应代码 `connect()`、`accept()` 执行阶段；

- 四次挥手：底层自动完成，对应代码 `close()` 关闭套接字阶段；

- TCP粘包、半包、连接异常，本质均源于TCP**流式无边界、面向连接**的特性。

# 第二章 原生TCP阻塞编程完整流程（标准五步）

TCP是面向连接的可靠协议，服务端有**固定五步标准流程**，客户端为简化三步流程，是所有TCP并发编程的基础。

![image-20260808160042730](https://cdn.llfc.club/image-20260808160042730.png)

##  TCP服务端标准五步流程

**创建Socket → 绑定IP和端口\(bind\) → 开启监听\(listen\) → 接受客户端连接\(accept\) → 读写数据\(recv/send\)**

###  流程逐步骤原理

- **1\. 创建Socket**：调用socket库，创建TCP流式套接字，开辟网络通信内存空间

- **2\. 绑定\(bind\)**：将套接字与本机IP、端口绑定，对外开放服务地址，固定通信入口

- **3\. 监听\(listen\)**：将主动套接字转为被动监听套接字，开启客户端连接监听，设置等待队列长度

- **4\. 接受连接\(accept\)**：阻塞等待客户端连接，连接成功后返回新通信套接字与客户端地址

- **5\. 读写数据**：通过新套接字完成数据接收\(recv\)、数据发送\(send\)，通信结束关闭套接字

###  完整可运行服务端代码

```python
'''
演示阻塞TCP服务器
'''

import socket

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
        while True:
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
            handle_client(conn,client_addr)
        except Exception as e:
            print(e)
            break


if __name__ == '__main__':
    # 1.创建socket和绑定监听
    server_socket = create_bind()
    # 2. 循环接受连接，并且处理读写
    server_loop(server_socket)

```

##  TCP客户端标准流程

**创建Socket → 连接服务端\(connect\) → 读写数据**

```python
'''
演示阻塞通信的TCP客户端
'''

import socket
# 1.创建TCP套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 2.连接服务器
server_host = '127.0.0.1'
server_port = 8888
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
```

##  原生阻塞TCP核心缺陷

原生TCP为**单线程阻塞模型**，存在两处核心阻塞点：`accept()`无连接阻塞、`recv()`无数据阻塞。同一时间只能处理**一个客户端**，必须等待当前客户端断开，才能处理下一个客户端，无法实现并发通信。

# 第三章 多线程TCP并发编程

为解决原生TCP单连接阻塞问题，引入多线程模型。核心思路：**主线程负责监听接收连接，每接入一个客户端，开辟独立子线程处理通信**，线程之间互不阻塞，实现多客户端并发。

##  核心原理

- 主线程：只循环执行`accept()`，持续接收新客户端连接，不处理数据通信

- 子线程：单个子线程绑定一个客户端，独立完成`recv/send`数据读写

- 线程隔离：不同客户端的通信逻辑独立运行，互不干扰，彻底解决单连接阻塞问题

## 完整可运行多线程TCP服务端代码

```python
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

```

##  多线程TCP优缺点

### 优点

- 解决单客户端阻塞问题，支持多客户端并发通信

- 代码逻辑简单、通俗易懂、稳定性强，适配中小型并发场景

### 缺点

- 线程属于系统重量级资源，连接数量过多时，线程频繁创建销毁会消耗大量CPU、内存

- 存在线程上下文切换开销，单机并发上限低（仅支持几百\~一千连接）

- 无法支撑高并发、长连接业务场景

# 第四章 协程异步TCP编程（高性能最优解）

为解决多线程资源开销大、并发上限低的问题，引入**asyncio协程异步模型**。底层基于IO多路复用，单线程实现高并发，是目前Python TCP高性能开发的主流方案。

## socket就绪概念

![image-20260812095305221](https://cdn.llfc.club/image-20260812095305221.png)

##  核心原理

- 全程**单线程运行**，无需创建多线程，无线程资源开销和切换损耗

- 通过**事件循环\+协程调度**管理所有客户端连接

- 遇到IO等待（等待客户端数据）时，协程主动让出CPU，调度处理其他就绪连接，最大化利用资源

- 以协程为并发单位，极轻量，单机可支撑十万级并发连接

## 完整可运行协程TCP服务端代码

```python
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

```

##  协程TCP优缺点与适用场景

### 优点

- 单线程支撑十万级高并发，资源占用极低，CPU利用率极高

- 协程为用户态轻量任务，无线程切换开销，调度效率远超多线程

- 代码顺序编写，逻辑清晰，可读性远优于IO多路复用回调写法

### 注意事项

- 事件循环为单线程，代码中不能出现耗时同步操作（会卡死整个服务）

- 需遵循异步编程规范，所有IO操作必须使用await修饰

### 适用场景

线上高性能服务、IM聊天服务、物联网长连接、高并发爬虫、后端接口服务等场景。

# 第五章 三种TCP模型核心对比总结

| 编程模型    | 并发方式       | 并发上限       | 资源开销         | 适用场景                       |
| ----------- | -------------- | -------------- | ---------------- | ------------------------------ |
| 原生阻塞TCP | 单线程串行     | 仅单连接       | 极低             | 本地简单测试、一对一短连接工具 |
| 多线程TCP   | 多线程并发     | 几百\~一千连接 | 较高（线程开销） | 低并发内网服务、小型业务服务   |
| 协程异步TCP | 单线程协程调度 | 十万级高并发   | 极低             | 线上高性能、高并发生产服务     |

# 第六章 工业级全双工 TCP 服务器（协程 \+ TLV协议 \+ 消息队列解耦）

前面章节的基础协程TCP仅实现基础收发，存在**TCP粘包、消息边界混乱、收发逻辑耦合、无法处理半包数据**等生产缺陷。本章实现企业级标准TCP服务：**全双工通信、TLV自定义协议解析、半包缓存续收、IO协程与逻辑协程分离、消息队列解耦**，是目前商用长连接服务器的标准架构。



## TCP粘包和断包

![image-20260812104519712](https://cdn.llfc.club/image-20260812104519712.png)





## TLV协议

TLV = Type(消息id) + Length(消息长度) + Value(消息的内容)

 Type(消息id) + Length(消息长度) = 数据包的包头(head)



![image-20260812105511001](https://cdn.llfc.club/image-20260812105511001.png)



比如想要发送Hello

id = 1001表示聊天消息

length = 5

data = 'Hello'



服务器接受数据，如果收到的数据长度大于等于头部长度4个字节，说明头部接收完整

解析头部，获取id(1001)和数据包的长度(5)

接下来继续判断收到的数据(扣除头部长度后)是否大于数据包的长度，如果大于则说明数据包的包体接受完全

否则就继续接受

##  核心架构设计

###  全双工定义

全双工TCP：客户端与服务端可**同时收发数据**，互不阻塞、互不干扰，区别于半双工的交替通信模式。基于协程分离读写任务，实现真正全双工。

### TLV自定义通信协议（解决粘包/半包核心）

自定义固定格式协议，彻底解决TCP流式无边界问题，保证消息完整解析，格式如下：

- **T \(Type/消息ID\)**：2字节，标识消息业务类型（如1=聊天消息、2=心跳包、3=指令请求）

- **L \(Length/消息长度\)**：2字节，标识后续Value数据的总长度

- **V \(Value/消息内容\)**：可变长度，真实业务数据（字符串/JSON/二进制数据）

完整数据包结构：`[2字节T][2字节L][N字节V]`

###  协程架构分离设计

采用**多协程分工**，彻底解耦IO读写与业务逻辑，避免业务阻塞网络收发：

1. **接收协程**：持续监听客户端数据，缓存半包数据、解析完整TLV消息，将合法消息放入全局逻辑队列

2. **逻辑处理协程**：独立消费队列消息，执行业务计算、数据处理，生成响应数据

3. **发送协程**：统一处理响应数据，封装TLV协议并发送给客户端，保证发送有序性

## 核心工具类（TLV编解码 + 半包缓存）

实现消息打包、解包、半包数据缓存续收，无完整数据包时保留数据，等待下一次接收补齐。

```python
import struct
import asyncio
from asyncio import Queue

# 全局业务消息队列：IO协程生产消息，逻辑协程消费消息
MSG_QUEUE = Queue(maxsize=1000)

class TLVProtocol:
    # T=2字节，L=2字节，头部固定4字节
    HEADER_LEN = 4

    @classmethod
    def encode(cls, msg_type: int, body: str) -> bytes:
        """
        TLV消息打包：对外发送完整数据包
        :param msg_type: 消息ID(T)
        :param body: 业务消息内容(V)
        :return: 二进制TLV数据包
        """
        body_bytes = body.encode("utf-8")
        body_len = len(body_bytes)
        # 网络字节序打包：2字节消息类型 + 2字节消息长度
        header = struct.pack("!HH", msg_type, body_len)
        return header + body_bytes

    @classmethod
    def decode(cls, buffer: bytes) -> tuple[list[dict], bytes]:
        """
        TLV消息解包：处理缓冲区数据，解析完整消息，返回未用完的半包数据
        :param buffer: 累计接收的缓冲区原始字节
        :return: 完整消息列表、剩余半包数据
        """
        messages = []
        # 循环解析，支持一次多条消息+半包残留
        while len(buffer) >= cls.HEADER_LEN:
            # 解析头部，获取消息体长度
            msg_type, body_len = struct.unpack("!HH", buffer[:cls.HEADER_LEN])
            total_pkg_len = cls.HEADER_LEN + body_len

            # 数据不完整，直接退出，保留当前所有数据等待下次接收
            if len(buffer) < total_pkg_len:
                break

            # 截取完整消息体
            body_data = buffer[cls.HEADER_LEN:total_pkg_len].decode("utf-8")
            messages.append({
                "msg_type": msg_type,
                "body": body_data,
                "body_len": body_len
            })
            # 截断已解析数据，保留剩余字节继续解析
            buffer = buffer[total_pkg_len:]
        return messages, buffer

```

##  全双工协程TCP服务完整实现

核心特性：半包数据持久缓存、收发全双工并行、业务逻辑队列解耦、异常重连容错、TLV严格协议校验

```python
import asyncio
from typing import Dict
# 导入上方TLV工具与全局队列
# 客户端连接池：保存所有在线客户端读写对象
CLIENT_POOL: Dict[str, asyncio.StreamWriter] = dict()

async def client_logic_worker():
    """
    全局逻辑处理协程（独立后台线程）
    专门消费消息队列，执行业务逻辑，不阻塞网络IO
    """
    print("业务逻辑处理协程启动成功")
    while True:
        # 阻塞获取队列消息
        msg_info = await MSG_QUEUE.get()
        client_addr = msg_info["client_addr"]
        msg_type = msg_info["msg_type"]
        msg_body = msg_info["body"]

        # ========== 自定义业务逻辑区域 ==========
        print(f"【业务处理】客户端{client_addr} 消息类型:{msg_type} 内容:{msg_body}")
        # 根据消息ID(T)分发不同业务
        if msg_type == 1:
            resp_body = f"[聊天回执]已收到消息：{msg_body}"
        elif msg_type == 2:
            resp_body = f"[心跳回执]心跳检测正常"
        else:
            resp_body = f"[未知指令]暂不支持消息类型{msg_type}"
        # ======================================

        # 封装响应消息，交给发送协程
        if client_addr in CLIENT_POOL:
            resp_pkg = TLVProtocol.encode(msg_type=msg_type, body=resp_body)
            writer = CLIENT_POOL[client_addr]
            writer.write(resp_pkg)
            await writer.drain()

        # 标记队列任务完成
        MSG_QUEUE.task_done()

async def client_handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """单个客户端连接总调度协程"""
    client_addr = f"{writer.get_extra_info('peername')}"
    CLIENT_POOL[client_addr] = writer
    print(f"新客户端接入：{client_addr}，当前在线：{len(CLIENT_POOL)}")

    # 客户端私有缓冲区：永久保存半包数据，直至数据接收完整
    recv_buffer = b""

    try:
        while True:
            # 异步接收数据，单次最大4096字节
            recv_data = await reader.read(4096)
            if not recv_data:
                break  # 客户端主动断开连接

            # 累加数据到缓冲区（保留上次半包数据）
            recv_buffer += recv_data

            # TLV解析：获取完整消息、剩余半包数据
            full_msgs, recv_buffer = TLVProtocol.decode(recv_buffer)

            # 完整消息全部投入逻辑队列，交由后台协程处理
            for msg in full_msgs:
                msg["client_addr"] = client_addr
                await MSG_QUEUE.put(msg)

    except Exception as e:
        print(f"客户端{client_addr}连接异常：{e}")
    finally:
        # 连接断开，清理资源
        del CLIENT_POOL[client_addr]
        writer.close()
        await writer.wait_closed()
        print(f"客户端{client_addr}已断开，当前在线：{len(CLIENT_POOL)}")

async def main():
    # 启动后台业务逻辑协程（常驻运行）
    asyncio.create_task(client_logic_worker())

    # 启动TLV-TCP服务
    server = await asyncio.start_server(
        client_handle,
        host="0.0.0.0",
        port=8888
    )
    print("【工业级TLV全双工TCP服务启动成功】")
    print("服务监听端口：8888 | 协议格式：T(2B)+L(2B)+V(NB)")

    await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())

```



### 格式符 !HH 逐段拆解

> ! 表示网络字节序（大端 big‑endian），网络都是使用大端字节序

大端字节序，高位存放低字节，低位存放高字节



![image-20260812111251238](https://cdn.llfc.club/image-20260812111251238.png)

判断存储模式，可以用一个字节存储1，表示0x00000001, 如果低地址存储的是1就是小端，高地址存储的是1就是大端

### 为什么会有字节序？

因为不同机器型号不同，存储的数据方式也不一样，所以就出现了大端存储和小端存储的差别了

为了统一口径，让对方准确识别我们发送的数据格式，就以大端模式作为标准了

![image-20260812111728020](https://cdn.llfc.club/image-20260812111728020.png)

Python中通过`!`表示大端

###  第一个 `H`

```
H → unsigned short，无符号短整型，占用 2 字节，取值范围 0 ~ 65535
```

###  第二个 `H`

第二个 2 字节无符号短整型

> `!HH` = 大端、2 个 short，头部总长度 = 2+2 = **4 bytes**



## 配套TLV协议客户端测试代码

用于测试服务端粘包解析、半包续收、队列处理、全双工通信能力

```python
import asyncio
from 第六章TLV全双工TCP import TLVProtocol

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

```

##  核心关键特性详解（生产重点）

###  半包续收机制

每个客户端独立绑定**私有缓冲区**，每次接收的数据都会累加至缓冲区。若数据不足一个完整TLV包，不丢弃、不报错，保留剩余数据，等待下一次循环接收数据后继续拼接解析，彻底解决TCP半包数据丢失问题。

### TLV协议防粘包原理

通过固定头部长度\+动态数据长度，精准切割消息边界：接收端先读取4字节头部，获取消息体真实长度，再精准截取对应数据，无论单次接收多少字节、是否粘连多条消息，均可精准解析。

###  协程队列解耦架构优势

- **IO与逻辑分离**：网络接收协程只做数据读取、解析、入队，不执行业务计算，保证网络IO永不阻塞

- **削峰填谷**：突发海量消息可存入队列，避免服务崩溃，平稳消费处理

- **全双工并行**：收发、业务处理三者并行执行，无交替阻塞，是标准服务器全双工模型

##  四种TCP模型最终终极对比

| TCP模型                | 粘包处理             | 并发能力           | 业务解耦        | 生产可用           |
| ---------------------- | -------------------- | ------------------ | --------------- | ------------------ |
| 原生阻塞TCP            | 无处理，存在严重粘包 | 单连接、无并发     | 完全耦合        | 仅测试使用         |
| 多线程TCP              | 无处理               | 低并发、线程上限低 | 线程内耦合      | 小型内网服务       |
| 基础协程TCP            | 无处理               | 十万级高并发       | 轻度耦合        | 简单业务场景       |
| TLV协程队列TCP（本章） | 完美解决粘包/半包    | 十万级高并发       | IO/逻辑完全解耦 | **工业级生产可用** |
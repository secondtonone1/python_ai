import  multiprocessing

def pipe_child(conn):
    '''
    子进程执行的函数
    :param conn: 孩子端
    :return: None
    '''
    # 子进程发送数据
    conn.send('子进程消息1')
    # 子进程从管道中读取信息，如果主进程没有发送消息，则阻塞
    print(f'子进程收到: {conn.recv()}')
    conn.close()

if __name__ == '__main__':
    # 创建管道, 返回两端连接对象
    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=pipe_child, args=(child_conn,))
    p.start()

    # 主进程接受信息，如果子进程没有发送信息，则主进程阻塞
    print(f'主进程收到: {parent_conn.recv()}')
    parent_conn.send('主进程回复信息')
    p.join()
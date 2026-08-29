'''
SmartService AI 智能客服系统 - 启动入口
========================================
用法 (在 ai_service 目录下执行):
    python run.py             # 启动服务
    python run.py --reload    # 开发模式(改代码自动重启)
    python run.py --port 9000 # 指定端口

启动前请确认:
    1. 已安装依赖: pip install -r requirements.txt
    2. 已初始化数据库: 执行 scripts/init_db.sql
'''
import argparse

import uvicorn

from aiservice.common.config import Config


def parse_args():
    parser = argparse.ArgumentParser(description='SmartService AI 智能客服系统')
    parser.add_argument('--host', default=None, help='监听地址 (默认读取 config.json)')
    parser.add_argument('--port', type=int, default=None, help='监听端口 (默认读取 config.json)')
    parser.add_argument('--reload', action='store_true', help='开发模式: 代码变更自动重启')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = Config.instance()
    host = args.host or str(config.get('server.host', '0.0.0.0'))
    port = args.port or int(config.get('server.port', 8000))
    reload_mode = args.reload or bool(config.get('server.reload', False))

    # uvicorn 以 "模块:实例" 字符串方式导入应用 (生产常用方式, 支持 reload)
    uvicorn.run('aiservice.main:app', host=host, port=port, reload=reload_mode)


if __name__ == '__main__':
    main()

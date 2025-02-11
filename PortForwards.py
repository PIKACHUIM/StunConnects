import asyncio


async def handle_client(reader, writer):
    """
    处理客户端连接，将数据转发到远程服务器
    """
    remote_reader, remote_writer = await asyncio.open_connection(
        remote_host, remote_port
    )
    print(f"Connected to remote server {remote_host}:{remote_port}")

    async def forward(source, target):
        """
        将数据从一个流转发到另一个流
        """
        try:
            while True:
                data = await source.read(4096)
                if not data:
                    break
                target.write(data)
                await target.drain()
        except Exception as e:
            print(f"Error in forward: {e}")
        finally:
            target.close()

    # 创建两个任务分别处理双向数据转发
    task1 = asyncio.create_task(forward(reader, remote_writer))
    task2 = asyncio.create_task(forward(remote_reader, writer))

    # 等待两个任务完成
    await asyncio.gather(task1, task2)


async def start_proxy(local_host, local_port, remote_host, remote_port):
    """
    启动TCP代理
    """
    server = await asyncio.start_server(
        handle_client, local_host, local_port
    )
    print(f"Listening on {local_host}:{local_port}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    local_host = "127.0.0.1"  # 本地监听地址
    local_port = 8080  # 本地监听端口
    remote_host = "9.134.240.153"  # 远程服务器地址
    remote_port = 1888  # 远程服务器端口
    asyncio.run(start_proxy(local_host, local_port, remote_host, remote_port))

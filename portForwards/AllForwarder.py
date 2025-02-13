import asyncio
import time

import requests
import multiprocessing
import threading
from portForwards.UdpForwarder import UdpForwarder

# class PortForwards(threading.Thread):
class PortForwards(multiprocessing.Process):
    def __init__(self,

                 local_port: str,  # 本地-端口
                 local_host: str = "127.0.0.1",
                 proxy_port: str = "",  # 端口
                 proxy_host: str = "",  # 地址
                 proxy_type: str = "TCP",
                 proxy_urls: str = None):
        super().__init__()
        self.proxy_port = str(proxy_port)
        self.proxy_host = str(proxy_host)
        self.local_port = str(local_port)
        self.local_host = str(local_host)
        self.proxy_type = str(proxy_type)
        self.proxy_urls = proxy_urls
        self.server_api = None
        self.loop = None  # 用于保存 asyncio 的事件循环
        self.flag = True  # 用于停止线程

    def run(self):
        self.url(self.proxy_urls)
        self.loop = asyncio.new_event_loop()  # 创建新的事件循环
        asyncio.set_event_loop(self.loop)  # 设置为当前线程的事件循环
        self.loop.run_until_complete(self.open())  # 启动异步任务

    def end(self):
        self.flag = False
        if self.server_api:
            self.server_api.close()  # 关闭服务器
        if self.loop:
            for task in asyncio.all_tasks(self.loop):
                task.cancel()
            self.loop.stop()  # 停止事件循环
            # self.loop.close()  # 关闭事件循环
        self.join()  # 等待线程结束

    def url(self, proxy_urls):
        if proxy_urls is not None:
            try:
                response = requests.get(
                    proxy_urls, allow_redirects=False)
                if response.status_code in (301, 302):
                    location = response.headers.get('Location')
                else:
                    location = response.text
                location = location.split("://")[1].split("/")[0]
                print("Remote:", response.status_code, location)
                self.proxy_host = location.split(":")[0]
                self.proxy_port = location.split(":")[1]
            except requests.RequestException as e:
                print(f"请求出错：{e}")
            except (IndexError, ValueError, Exception) as e:
                print(f"解析出错：{e}")

    # 启动代理 #######################################################
    async def open(self):
        if self.proxy_type == "TCP":
            # 启动TCP代理 ============================================
            self.server_api = await asyncio.start_server(
                self._tcp, self.local_host, self.local_port)
            print("Listen:", self.proxy_type,
                  self.local_host + ":" + self.local_port)
            async with self.server_api:
                await self.server_api.serve_forever()
        elif self.proxy_type == "UDP":
            # 启动UDP代理 ============================================
            loop = asyncio.get_running_loop()
            self.server_api, _ = await loop.create_datagram_endpoint(
                lambda: UdpForwarder(
                    self.proxy_host, self.proxy_port,
                    self.local_host, self.local_port,
                ),
                local_addr=(self.local_host, int(self.local_port))
            )
            print("Listen:", self.proxy_type,
                  self.local_host + ":" + self.local_port)
            await asyncio.sleep(3600)  # 保持运行，可以调整为其他方式
        else:
            raise ValueError("Unsupported type. Use 'TCP' or 'UDP'.")

    # TCP4连接 #######################################################
    async def _tcp(self, reader, writer):
        # 处理客户端连接，将数据转发到远程服务器 =====================
        remote_reader, remote_writer = await asyncio.open_connection(
            self.proxy_host, self.proxy_port)

        # print("Server:", self.proxy_host + ":" + self.proxy_port)

        # 处理数据流转发 =============================================
        async def forward(source, target):
            try:  # 将数据从一个流转发到另一个流 ---------------------
                while self.flag:
                    data = await source.read(4096)
                    if not data:
                        break
                    target.write(data)
                    await target.drain()
            except Exception as e:
                print(f"Error in forward: {e}")
            finally:
                target.close()

        # 创建两个任务分别处理双向数据转发 ===========================
        task1 = asyncio.create_task(forward(reader, remote_writer))
        task2 = asyncio.create_task(forward(remote_reader, writer))
        # 等待两个任务完成 ===========================================
        await asyncio.gather(task1, task2)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    port = PortForwards(
        "8080", "127.0.0.1",
        "1080", "10.1.1.1",
        "TCP")
    port.start()
    time.sleep(10)
    port.kill()
    # port.end()

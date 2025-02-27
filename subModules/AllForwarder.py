import asyncio
import os
import subprocess
import sys
import time
import requests
import flet as ft
import multiprocessing

from subModules.LogRecorders import Log, LL as L
from subModules.TimeWatchers import PortWatchers
from subModules.UdpForwarder import UdpForwarder


class PortForwards(multiprocessing.Process):
    def __init__(self,  # 核心参数 ===========
                 local_port: str,  # 本地-端口
                 local_host: str = "127.0.0.1",
                 proxy_port: str = "",  # 端口
                 proxy_host: str = "",  # 地址
                 proxy_type: str = "",  # 协议
                 proxy_urls: str = "",  # 链接
                 # 可选参数 ==================
                 super_type=None,  # 主程序API
                 socat_flag=None,  # 主程序API
                 pkill_flag=None,  # 标识符API
                 in_log_api=None,  # 日志的API
                 in_dog_var=1800,  # 自检查API
                 server_tip="StunConnects"):
        super().__init__()
        # 核心内容 ===========================
        self.proxy_port = str(proxy_port)
        self.proxy_host = str(proxy_host)
        self.local_port = str(local_port)
        self.local_host = str(local_host)
        self.proxy_type = str(proxy_type)
        self.proxy_urls = proxy_urls
        self.super_type = super_type
        self.socat_flag = socat_flag
        self.pkill_flag = pkill_flag
        # 内部接口 ============================
        self.proxy_proc = {}
        self.server_tcp = None
        self.server_udp = None
        # 内部信息 ============================
        self.time = in_dog_var  # 自更新
        self.logs = in_log_api  # 输出行
        self.loop = None  # 保存事件循环
        self.flag = True  # 任务执行标记
        self.done = None  # 任务执行标记
        self.text = None  # 任务执行标记
        # 日志创建 ============================
        if self.logs is None:
            self.logs = Log(
                server_tip,
                server_tip,
                server_tip).log
        self.dogs = None
        ########################################################

    # 开始转发 #################################################
    def run(self):
        LT = "start_url_ap"
        self.pulled(self.proxy_urls)  # 获取地址失败，终止此任务
        # 获取地址成功，启动任务 ===============================
        self.done = self.flag = True  # 标记任务执行允许启动事件
        # 看门狗 ===============================================
        self.dogs = PortWatchers(self, self.time, self.logs)  ##
        self.dogs.start()  # 启动定期检查看门狗子进程 ==========
        # Android ==============================================
        if self.socat_flag:
            self.socat_all_proxy()
            return True
        # 其他平台 =============================================
        self.loop = asyncio.new_event_loop()  # 创建新的事件循环
        asyncio.set_event_loop(self.loop)  # 设置-当前线程的事件
        try:  # 启动主转发进程 =================================
            self.loop.run_until_complete(self.open())  # asyncio
        except (ConnectionResetError, Exception) as err:
            self.logs("Killed: " + str(err), LT, L.D)

    # 结束转发 #################################################
    def end(self):
        self.flag = self.flag = False
        for proxy_now in self.proxy_proc:
            import psutil
            parent = psutil.Process(self.proxy_proc[proxy_now].pid)
            # 终止所有子进程
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
        for server_str in (self.server_tcp, self.server_udp):
            if server_str:
                server_str.close()
                time.sleep(5)
        self.server_tcp = self.server_udp = None

    # 重载转发 #################################################
    def reload(self):
        LT = "check_url_ap"
        if not self.pulled(self.proxy_urls):
            local_ap = self.proxy_host + ":" + self.proxy_port
            self.logs("Change: " + local_ap, LT, L.G_)
            self.end()
            sys.exit(5)

    # 拉取信息 ######################################################
    def pulled(self, proxy_urls):
        LT = "get_url_text"
        if proxy_urls is None:
            sys.exit(1)
        try:
            self.logs("解析地址: %s" % proxy_urls, LT, L.M)
            retry = 10
            while True:
                if retry < 0:
                    sys.exit(4)
                try:
                    response = requests.get(
                        proxy_urls, allow_redirects=False, timeout=30)
                    break
                except requests.ConnectTimeout as err:
                    self.logs("Errors: %s" % str(err), LT, L.W)
                    time.sleep(1)
                    retry -= 1
            # 判断状态 ===============================================
            location = response.text
            if response.status_code in (301, 302):
                location = response.headers.get('Location')
            location = location.split("://")[1].split("/")[0]
            local_ap = self.proxy_host + ":" + self.proxy_port
            self.logs("远程端口: %s %s" % (
                str(response.status_code), location), LT, L.M)
            if len(local_ap) > 5:
                self.logs("本地端口: %s %s" % (
                    str(response.status_code), local_ap), LT, L.M)
            self.proxy_host = location.split(":")[0]
            self.proxy_port = location.split(":")[1]
            return local_ap == location
        except requests.RequestException as e:
            self.logs(f"请求出错：{e}", LT, L.M)
            self.text = "请求出错：" + str(e)
            sys.exit(1)
        except (IndexError, ValueError, Exception) as e:
            self.logs(f"解析出错：{e}", LT, L.M)
            self.text = "解析出错：" + str(e)
            sys.exit(2)

    # socat代理模式 =================================================
    def socat_all_proxy(self):
        LT = "socat_proxys"
        proxy_arch = {
            ft.PagePlatform.ANDROID: "linux.a64",
            ft.PagePlatform.WINDOWS: "win64.exe",
            ft.PagePlatform.MACOS: "macos.x64",
            ft.PagePlatform.LINUX: "linux.x64",
        }
        socat_arch = proxy_arch[self.super_type]
        for listen_str in ("TCP", "UDP"):
            tmp = ("socat.%s %s4-LISTEN:%s,reuseaddr,fork %s4:%s:%s" % (
                socat_arch, listen_str, self.local_port,
                listen_str, self.proxy_host, self.proxy_port))
            self.logs("监听命令： " + tmp, LT, L.D)
            proc = subprocess.Popen(
                tmp, shell=True, cwd="./appSources/Socat")
            self.proxy_proc[listen_str] = proc
        while self.pkill_flag is None or not self.pkill_flag.is_set():
            time.sleep(0.1)
        self.end()

    # proxy代理模式 =================================================
    async def start_tcp_proxy(self):
        LT = "start_tcp_ap"
        # 启动TCP代理 ===============================================
        retry = 10
        while True:
            if retry < 0:
                sys.exit(5)
            try:
                self.logs("监听端口: TCP %s:%s" % (
                    self.local_host, self.local_port), LT, L.S)
                self.server_tcp = await asyncio.start_server(
                    self._tcp, self.local_host, self.local_port)
                async with self.server_tcp:
                    await self.server_tcp.serve_forever()
                break
            except (OSError, asyncio.exceptions, Exception) as err:
                self.logs("Errors：TCP " + str(err), LT, L.W)
                time.sleep(1)
                retry -= 1

    # proxy代理模式 =================================================
    # noinspection PyTypeChecker
    async def start_udp_proxy(self):
        LT = "start_udp_ap"
        # 启动UDP代理 ===============================================
        loop = asyncio.get_running_loop()
        retry = 10
        while True:
            if retry < 0:
                exit(5)
            try:
                self.logs("监听端口: UDP %s:%s" % (
                    self.local_host, self.local_port), LT, L.S)
                self.server_udp, _ = await \
                    loop.create_datagram_endpoint(
                        lambda: UdpForwarder(
                            self.proxy_host, self.proxy_port,
                            self.local_host, self.local_port, self.logs),
                        local_addr=(self.local_host, int(self.local_port)))
                break
            except (OSError, Exception) as err:
                self.logs("Errors：TCP " + str(err), LT, L.W)
                time.sleep(1)
                retry -= 1
        await asyncio.sleep(86400)  # 保持运行，可以调整为其他方式

    # 启动代理 #######################################################
    async def open(self):
        if self.proxy_type == "All":
            await asyncio.gather(
                self.start_tcp_proxy(), self.start_udp_proxy())
        elif self.proxy_type == "TCP":
            await self.start_tcp_proxy()
        if self.proxy_type == "UDP":
            await self.start_udp_proxy()

    # TCP4连接 #######################################################
    async def _tcp(self, reader, writer):
        LT = "proxy_tcp_ap"
        try:
            # 处理客户端连接，将数据转发到远程服务器 =================
            remote_reader, remote_writer = await \
                asyncio.open_connection(
                    self.proxy_host, self.proxy_port)

            # 处理数据流转发 =========================================
            async def forward(source, target):
                try:  # 将数据从一个流转发到另一个流 -----------------
                    while self.flag:
                        data = await source.read(4096)
                        if not data:
                            break
                        target.write(data)
                        await target.drain()
                except Exception as e:
                    self.logs("Errors: %s" % str(e), LT, L.E)
                    sys.exit(3)
                finally:
                    target.close()
                    sys.exit(4)

            # 创建两个任务分别处理双向数据转发 ===========================
            task1 = asyncio.create_task(forward(reader, remote_writer))
            task2 = asyncio.create_task(forward(remote_reader, writer))
            # 等待两个任务完成 ===========================================
            await asyncio.gather(task1, task2)
        except (OSError, Exception) as e:
            self.logs("Errors：TCP " + str(e), LT, L.W)
            exit(5)


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

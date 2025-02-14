# UDP 数据转发处理器 #################################################################
class UdpForwarder:
    # 初始化接口 #####################################################################
    def __init__(self,
                 proxy_host,
                 proxy_port,
                 local_host,
                 local_port):
        self.proxy_port = int(proxy_port)  # OLD
        self.local_port = int(local_port)  # NEW
        self.proxy_host = proxy_host  # 远程端口
        self.local_host = local_host  # 监听端口
        self.start_host = None  # 记录来访问端口
        self.start_port = None  # 记录来访问端口
        self.transports = None  # 记录来访问信息

    # 初始化连接 #####################################################################
    def connection_made(self, transport):
        self.transports = transport

    # 处理数据流 #####################################################################
    def datagram_received(self, data, addr):
        # print(f"Received UDP data from {addr}: {data}")
        # print(self.proxy_host, self.proxy_port)
        # print(self.local_host, self.local_port)
        # 判断来源IP信息 =============================================================
        if len(addr) < 2 or addr[0] is None or addr[1] is None:  # 无效IP:PORT送回远端
            self.transports.sendto(data, (self.proxy_host, self.proxy_port))  # 发数据
        # 当来源主机端口等于本地监听，表明：本地-->远端（直接模式） ==================
        elif addr[0] == self.local_host and addr[1] == self.local_port:  # 本地-->远端
            self.transports.sendto(data, (self.proxy_host, self.proxy_port))  # 发数据
        # 当来源是被代理的主机和地址，表示：远端-->本地（主动模式） ==================
        elif addr[0] == self.proxy_host and addr[1] == self.proxy_port:  # 远端-->本地
            if self.start_host is None or self.start_port is None:  # 尚未建立连接 ===
                self.transports.sendto(data, (self.proxy_host, self.proxy_port))  # UP
            else:  # 将来自远端的数据发送到真实客户端口 ==============================
                self.transports.sendto(data, (self.start_host, self.start_port))  # IP
        # 当来源完全不匹配任何地址时，表示：本地-->远端（被动模式） ==================
        else:  # 将来客户端的数据发送到被代理的远端地址 ==============================
            self.transports.sendto(data, (self.proxy_host, self.proxy_port))  # 转发包
            self.start_port = addr[1]  # 记录/更新客户真实端口，以便远端发送数据后转发
            self.start_host = addr[0]  # 记录/更新客户真实地址，以便远端发送数据后转发

    # 遇到错误时 #####################################################################
    def error_received(self, exc):
        print(f"Error in UDP forward: {exc}")
        exit(3)

    # 连接丢失时 #####################################################################
    def connection_lost(self, exc):
        print("UDP connection lost")
        exit(4)

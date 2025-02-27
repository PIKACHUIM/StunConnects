import threading
import time
import flet as ft

from module.AllForwarder import PortForwards


class taskWatchers(threading.Thread):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.flag = True

    def run(self):
        exit_text = {
            1: "请求错误，请检查网络连接",
            2: "解析出错，请检查链接地址",
            3: "转发出错，请检查端口权限",
            4: "连接关闭，请检查网络连接",
            5: "监听错误，监听端口有错误",
            0: "未知错误",
        }
        while self.flag:
            time.sleep(1)
            if self.main.ports is None:
                return False
            if not self.main.ports.is_alive():
                print(self.main.ports.exitcode)
                if self.main.ports.exitcode not in exit_text:
                    return False
                if self.main.ports.exitcode == 5 \
                        or self.main.ports.exitcode == 0:
                    self.main.ports = PortForwards(
                        self.main.map_port_data,
                        "0.0.0.0",
                        super_type=self.main.super_type,
                        proxy_type=self.main.map_type_data,
                        proxy_urls=self.main.url_text_data,
                        socat_flag=self.main.socats_flag,
                        in_dog_var=self.main.time,
                        server_tip="StunConnects"
                    )
                    self.main.ports.start()
                    continue
                self.main.dlg_kill.content = ft.Text(
                    ("映射名称: %s\n"
                     "远程地址: %s\n"
                     "本地端口: 0.0.0.0:%s\n"
                     "错误信息: %s\n") % (
                        self.main.map_name_data,
                        self.main.url_text_data,
                        self.main.map_port_data,
                        # self.ports.text
                        exit_text[self.main.ports.exitcode]
                    )
                )
                self.main.map_open.value = False
                self.main.open_clicked(None)
                self.main.super.page.open(self.main.dlg_kill)
                self.main.update()
                return False

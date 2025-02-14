import os

import flet as ft
import pyperclip
from portForwards.AllForwarder import PortForwards
from portForwards.LoopForwarder import LoopForwarder


class Task(ft.Column):
    def __init__(self,
                 url_text,
                 map_name,
                 map_port,
                 map_type,
                 task_change,
                 task_delete,
                 host_locals,
                 in_super,
                 ):
        super().__init__()
        # 关键数据 =====================
        self.width = 720
        self.ports = None
        self.watch = None
        self.check = False
        self.super = in_super
        # 事件处理 =====================
        self.on_change = task_change
        self.on_delete = task_delete
        self.now_local = host_locals
        #  代理信息 ====================
        self.url_text_data = url_text
        self.map_name_data = map_name
        self.map_port_data = map_port
        self.map_type_data = map_type

        # 元素 #######################################
        # 代理名称 ===================================
        self.map_name = ft.Checkbox(
            width=100, value=False,
            label=map_name,
            on_change=self.item_clicked
        )
        # 设置名称 ===================================
        self.set_name = ft.TextField(
            width=90, label="备注名称",
            visible=False,
            value=map_name,
            border=ft.InputBorder.UNDERLINE
        )
        # 代理地址 ===================================
        self.url_text = ft.TextField(
            expand=True,
            # value=url_text.replace("https://", ""),
            value=url_text,
            hint_text="https://1web.us.kg/p/XXXXXXXX",
            border=ft.InputBorder.NONE,
            read_only=True,
        )
        # 代理端口 ===================================
        self.map_port = ft.TextField(
            width=60,
            value=map_port,
            # alue="127.0.0.1:" + str(map_port),
            border=ft.InputBorder.NONE,
            read_only=True,
        )
        # 代理类型 ===================================
        self.map_type = ft.Dropdown(
            width=60,
            value=map_type,
            options=[
                ft.dropdown.Option("All"),
                ft.dropdown.Option("TCP"),
                ft.dropdown.Option("UDP"),
            ],
            border=ft.InputBorder.NONE,
            disabled=True,
        )
        # 代理开关 ===================================
        self.map_open = ft.Switch(
            # label=" ✔️",
            label="",
            on_change=self.open_clicked,
            value=True,
        )
        # 代理删除 ===================================
        self.map_kill = ft.IconButton(
            ft.Icons.DELETE_ROUNDED,
            tooltip="删除当前映射",
            on_click=self.kill_clicked,
            disabled=True, visible=False
        )
        # 本机地址 ===================================
        self.url_copy = ft.IconButton(
            ft.Icons.COMPUTER_ROUNDED,
            tooltip="复制本机地址",
            on_click=lambda e: pyperclip.copy(
                "127.0.0.1:" +
                str(self.map_port.value)),
            disabled=False,
        )
        # 内网地址 ===================================
        self.url_pubs = ft.IconButton(
            ft.Icons.ROUTER_ROUNDED,
            tooltip="复制局域网IP",
            on_click=lambda e: pyperclip.copy(
                self.now_local + ":" +
                str(self.map_port.value)),
            disabled=False,
        )
        # 输出错误 ===================================
        self.dlg_kill = ft.AlertDialog(
            title=ft.Text("映射错误"),
            content=ft.Text(""),
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e:
                    self.super.page.close(
                        self.dlg_kill))
            ],
        )
        # 代理添加 ===================================
        self.controls = [
            ft.Row(
                controls=[
                    self.map_name,
                    self.set_name,
                    self.url_text,
                    self.map_port,
                    self.map_type,
                    self.url_copy,
                    self.url_pubs,
                    self.map_kill,
                    self.map_open,
                ],
            )
        ]
        # 内置接口 ====================================
        self.item_checked()
        self.open_mapping()

    # 切换 ####################################################################
    def open_clicked(self, e):
        # 关闭代理时 =======================================
        if not self.map_open.value:
            self.stop_mapping()  # 关闭代理
            # 允许编辑 --------------------------------------
            self.url_text.read_only = False
            self.map_port.read_only = False
            self.map_type.read_only = False
            self.map_kill.read_only = False
            self.url_text.label = "跳转链接"
            self.map_port.label = "本地端口"
            self.map_type.label = "映射类型"
            self.map_type.label = "映射类型"
            # 修改样试 ------------------------------------
            self.url_text.border = ft.InputBorder.UNDERLINE
            self.map_port.border = ft.InputBorder.UNDERLINE
            self.map_type.border = ft.InputBorder.UNDERLINE
            self.map_kill.border = ft.InputBorder.UNDERLINE
            # 修改按钮样式 --------------------------------
            self.map_kill.disabled = False
            self.map_type.disabled = False
            self.url_copy.disabled = True
            self.url_pubs.disabled = True
            # 修改宽度内容 ---------------------------------
            self.url_copy.visible = False
            self.url_pubs.visible = False
            # self.map_name.visible = False
            self.map_kill.visible = True
            self.set_name.visible = True
            # self.map_open.label = " ❌"
            # 设置名称 -------------------------------------
            self.set_name.value = self.map_name.label
            self.map_name.label = ""
            self.map_name.width = 20
        # 打开代理时 =======================================
        else:
            # 清空标签 -------------------------------------
            self.url_text.label = ""
            self.map_port.label = ""
            self.map_type.label = ""
            self.map_type.label = ""
            # 修改边框样式 ---------------------------------
            self.url_text.border = ft.InputBorder.NONE
            self.map_port.border = ft.InputBorder.NONE
            self.map_type.border = ft.InputBorder.NONE
            self.map_kill.border = ft.InputBorder.NONE
            # 修改只读状态 ---------------------------------
            self.url_text.read_only = True
            self.map_port.read_only = True
            self.map_type.read_only = True
            self.map_kill.read_only = True
            # 修改按钮样式 ---------------------------------
            self.map_kill.disabled = True
            self.map_type.disabled = True
            self.url_copy.disabled = False
            self.url_pubs.disabled = False
            # 修改宽度和内容 -------------------------------
            self.url_copy.visible = True
            self.url_pubs.visible = True
            # self.map_name.visible = True
            self.set_name.visible = False
            self.map_kill.visible = False
            # self.map_open.label = " ✔️"
            # 设置名称 -------------------------------------
            self.map_name.label = self.set_name.value
            self.map_name.width = 100
            # 启动代理 -------------------------------------
            self.open_mapping()
        # 更新界面 =========================================
        self.on_change(None)
        self.update()

    # 操作 ####################################################################
    def item_checked(self):
        # 检查内容 ===============================================
        if self.url_text.value.find("://") < 0:
            self.url_text.value = "https://" + self.url_text.value
        # 获取内容 -----------------------------------------------
        self.url_text_data = self.url_text.value
        self.map_name_data = self.map_name.value
        self.map_port_data = self.map_port.value
        self.map_type_data = self.map_type.value
        self.before_update()

    # 按钮 ####################################################################
    # 开始映射 ================================================================
    def open_mapping(self):
        if self.ports is None:
            self.ports = PortForwards(
                self.map_port_data,
                "0.0.0.0",
                proxy_type=self.map_type_data,
                proxy_urls=self.url_text_data)
            self.ports.start()
            self.watch = LoopForwarder(self)
            self.watch.start()

    # 停止映射 ================================================================
    def stop_mapping(self):
        # 停止代理 --------------------------------
        if self.ports is not None:
            self.watch.flag = False
            self.watch = None
            print("Killed:", self.map_type_data,
                  self.ports.local_host +
                  ":" + self.ports.local_port)
            self.ports.kill()
            self.ports = None

    # 删除映射 ================================================================
    def kill_clicked(self, e):
        self.stop_mapping()
        self.update()
        self.on_delete(self)

    # 选中映射 ================================================================
    def item_clicked(self, e):
        self.check = self.map_name.value
        self.on_change(e)


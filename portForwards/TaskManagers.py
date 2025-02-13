import flet as ft
import pyperclip
from portForwards.AllForwarder import PortForwards


class Task(ft.Column):
    def __init__(self,
                 url_text,
                 map_name,
                 map_port,
                 map_type,
                 task_change,
                 task_delete
                 ):
        super().__init__()
        self.port = None
        self.width = 700
        self.is_select = False
        self.on_change = task_change
        self.on_delete = task_delete

        #  代理信息 ====================
        self.url_text_data = url_text
        self.map_name_data = map_name
        self.map_port_data = map_port
        self.map_type_data = map_type

        # 内置接口 ======================
        self.open_mapping()

        self.map_name = ft.Checkbox(
            width=100, value=False,
            label=map_name,
            on_change=self.item_clicked
        )
        self.set_name = ft.TextField(
            width=80, label="备注名称",
            visible=False,
            value=map_name,
            border=ft.InputBorder.UNDERLINE
        )
        self.url_text = ft.TextField(
            expand=True,
            value=url_text.replace("https://", ""),
            hint_text="https://1web.us.kg/p/XXXXXXXX",
            border=ft.InputBorder.NONE,
            read_only=True,
        )
        self.map_port = ft.TextField(
            width=155,
            value="127.0.0.1:" + str(map_port),
            border=ft.InputBorder.NONE,
            read_only=True,
        )

        self.map_type = ft.Dropdown(
            width=60,
            value=map_type,
            options=[
                ft.dropdown.Option("TCP"),
                ft.dropdown.Option("UDP"),
            ],
            border=ft.InputBorder.NONE,
            disabled=True,
        )
        self.map_open = ft.Switch(
            label=" ✔️",
            on_change=self.open_clicked,
            value=True,
        )
        self.map_kill = ft.IconButton(
            ft.Icons.DELETE_ROUNDED,
            tooltip="Delete Mapping",
            on_click=self.kill_clicked,
            disabled=True, visible=False
        )
        self.url_copy = ft.IconButton(
            ft.Icons.CONTENT_COPY_ROUNDED,
            tooltip="Copy Host:Port",
            on_click=lambda e: pyperclip.copy(self.map_port.value),
            disabled=False,
        )
        self.controls = [
            ft.Row(
                controls=[
                    self.map_name,
                    self.set_name,
                    self.url_text,
                    self.map_port,
                    self.map_type,
                    self.url_copy,
                    self.map_kill,
                    self.map_open,
                ],
            )
        ]

    def open_clicked(self, e):
        if not self.map_open.value:
            self.kill_mapping()
            self.url_text.read_only = False
            self.map_port.read_only = False
            self.map_type.read_only = False
            self.map_kill.read_only = False
            self.url_text.label = "跳转链接"
            self.map_port.label = "本地端口"
            self.map_type.label = "映射类型"
            self.map_type.label = "映射类型"
            self.url_text.border = ft.InputBorder.UNDERLINE
            self.map_port.border = ft.InputBorder.UNDERLINE
            self.map_type.border = ft.InputBorder.UNDERLINE
            self.map_kill.border = ft.InputBorder.UNDERLINE
            self.map_kill.disabled = False
            self.map_type.disabled = False
            self.url_copy.disabled = True
            # 修改宽度和内容 -------------------------------
            self.map_port.width = 60
            self.map_port.value = self.map_port.value.replace("127.0.0.1:", "")
            self.url_copy.visible = False
            self.map_name.visible = False
            self.map_kill.visible = True
            self.set_name.visible = True
            self.set_name.value = self.map_name.value
            self.url_text.value = "https://" + self.url_text.value
            #
            self.map_open.label = " ❌"

        else:
            self.url_text.label = ""
            self.map_port.label = ""
            self.map_type.label = ""
            self.map_type.label = ""
            self.url_text.border = ft.InputBorder.NONE
            self.map_port.border = ft.InputBorder.NONE
            self.map_type.border = ft.InputBorder.NONE
            self.map_kill.border = ft.InputBorder.NONE
            self.url_text.read_only = True
            self.map_port.read_only = True
            self.map_type.read_only = True
            self.map_kill.read_only = True
            self.map_kill.disabled = True
            self.map_type.disabled = True
            self.url_copy.disabled = False
            # 修改宽度和内容 -------------------------------
            self.map_port.width = 155
            self.url_copy.visible = True
            self.map_name.visible = True
            self.set_name.visible = False
            self.map_kill.visible = False
            self.map_open.label = " ✔️"
            # self.map_open.label = ""
            self.map_name.value = self.set_name.value
            self.map_port.value = "127.0.0.1:" + self.map_port.value
            self.url_text.value = self.url_text.value.replace("https://", "")
            # 启动
            self.url_text_data = "https://" + self.url_text.value
            self.map_name_data = self.map_name.value
            self.map_port_data = self.map_port.value
            self.map_type_data = self.map_type.value
            self.open_mapping()
        self.update()

    def open_mapping(self):
        if self.port is None:
            self.port = PortForwards(
                self.map_port_data,
                "127.0.0.1",
                proxy_type=self.map_type_data,
                proxy_urls=self.url_text_data)
            self.port.start()

    def kill_mapping(self):
        if self.port is not None:
            print("Killed:", self.map_type_data,
                  self.port.local_host +
                  ":" + self.port.local_port)
            self.port.kill()
            self.port = None

    def kill_clicked(self, e):
        self.kill_mapping()
        self.update()
        self.on_delete(self)

    # 按钮 ####################################################################
    def item_clicked(self, e):
        self.is_select = self.map_name.value
        self.on_change(self)

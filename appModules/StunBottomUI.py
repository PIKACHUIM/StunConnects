import sys
import webbrowser

import flet as ft

from subModules.FindResource import FindResource


class StunBottomUI:
    @staticmethod
    def set_ui(self):
        # 过滤器 ----------------------------------------------
        self.count = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.task_changed,
            tabs=[ft.Tab(text="所有映射"),
                  ft.Tab(text="正在映射"),
                  ft.Tab(text="停止映射")], )
        # 启动 ------------------------------------------------
        self.open_map = ft.Button(
            text="启动", on_click=self.task_started,
            icon=ft.Icons.NOT_STARTED_ROUNDED,
            disabled=True,
            visible=not self.server_flag)
        # 停止 ------------------------------------------------
        self.stop_map = ft.Button(
            text="停止", on_click=self.task_stopped,
            icon=ft.Icons.STOP_ROUNDED,
            disabled=True,
            visible=not self.server_flag)
        # 删除 ------------------------------------------------
        self.kill_map = ft.Button(
            text="删除", on_click=self.task_clicked,
            icon=ft.Icons.DELETE_ROUNDED,
            disabled=True,
            visible=not self.server_flag)
        # 服务 ================================================
        self.demo_run = ft.Switch(
            label=" 已启用",
            on_change=lambda e: self.flag_service(
                e, f=self.demo_run.value),
            value=True,
            disabled=self.server_flag,
        )
        self.demo_dlg = ft.AlertDialog(
            title=ft.Text("服务状态"),
            content=ft.Column(controls=[
                ft.Row(controls=[
                    ft.Text("服务状态："),
                    self.demo_run
                ]),
                ft.Row(controls=[
                    ft.Text("应用更改："),
                    ft.Button(
                        text="重载服务端",
                        icon=ft.Icons.RESTART_ALT_ROUNDED,
                        on_click=self.save_configs,
                    )
                ]),
                ft.Row(controls=[
                    ft.Text("重启服务："),
                    ft.Button(
                        text="重启此服务",
                        icon=ft.Icons.RESTART_ALT_ROUNDED,
                        on_click=self.load_service,
                    )
                ]),
                ft.Row(controls=[
                    ft.Text("服务模式下更改不会立即生效\n"
                            "请点击[应用更改]让更改生效")]),
            ]),
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e: self.page.close(
                        self.demo_dlg))
            ],
        ) if sys.platform.startswith('win32') else ft.Container()
        self.demo_txt = ft.OutlinedButton(
            text="服务模式",
            visible=self.server_flag,
            icon=ft.Icons.MISCELLANEOUS_SERVICES_ROUNDED,
            on_click=lambda e: self.page.open(self.demo_dlg)
        ) if sys.platform.startswith('win32') else ft.Container()
        self.demo_set = ft.Button(
            text="应用更改",
            icon=ft.Icons.RESTART_ALT_ROUNDED,
            # visible=self.server_flag and not self.pages.platform == "web",
            visible=False,
            on_click=self.save_configs,
        ) if sys.platform.startswith('win32') else ft.Container()
        # 底部 --------------------------------------------
        self.item_num = ft.Text("0个已选中")
        self.push_set = ft.Button(
            text="设置",
            on_click=lambda e: self.page.open(self.dlg_conf),
            icon=ft.Icons.SETTINGS_ROUNDED, )
        self.push_use = ft.Button(
            text="教程",
            on_click=lambda e: webbrowser.open(
                "https://github.com/PIKACHUIM/StunConnects/blob/main/USAGES.MD"),
            icon=ft.Icons.BOOK_ROUNDED, )
        self.push_inf = ft.Button(
            text="关于",
            on_click=lambda e: self.page.open(self.dlg_info),
            icon=ft.Icons.INFO_ROUNDED, )
        self.push_url = ft.Button(
            text="Github",
            on_click=lambda e: webbrowser.open(
                "https://github.com/PIKACHUIM/StunConnects"),
            icon=ft.Icons.LINK_ROUNDED, )


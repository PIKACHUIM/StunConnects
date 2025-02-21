import os
import sys
import webbrowser

import flet as ft

from subModules.FindResource import FindResource


class StunConfigUI:
    @staticmethod
    def set_ui(self):
        # 设置开关 --------------------------------------------
        self.sys_auto = ft.Switch(
            value=self.starts_flag,
            label="已禁用",
            on_change=lambda e: self.conf_startup(e),
            disabled=self.server_flag
        )
        self.sys_demo = ft.Switch(
            value=self.server_flag,
            label="已禁用",
            on_change=lambda e: self.conf_service(e))

        # disabled=True
        # 设置时间 --------------------------------------------
        def new_time(e):
            self.update_time = self.set_time.value
            for task_now in self.tasks.controls:
                if task_now.ports is None:
                    continue
                if task_now.ports.dogs is None:
                    continue
                task_now.ports.dogs.time = self.set_time.value
            self.save_configs()

        self.set_time = ft.TextField(
            value=str(self.update_time),
            hint_text="600",
            text_align=ft.TextAlign.RIGHT,
            border=ft.InputBorder.UNDERLINE,
            width=85,
            on_change=new_time
        )

        # 设置页面 =============================================
        self.dlg_conf = ft.AlertDialog(
            title=ft.Text("设置"),
            content=ft.Column(controls=[ft.Row(controls=[
                # 更新周期 -------------------------------------
                ft.Text("自动更新周期："),
                self.set_time,
                ft.Text("秒")]),
                # 运行日志 -------------------------------------
                ft.Row(controls=[
                    ft.Text("查看运行日志："),
                    ft.Button(
                        text="查看日志",
                        icon=ft.Icons.LOGO_DEV_ROUNDED,
                        on_click=self.open_log_dlg,
                    )],
                    alignment=ft.MainAxisAlignment.START),
                # 服务安装 -------------------------------------
                ft.Row(controls=[
                    ft.Text("作为服务安装："),
                    self.sys_demo],
                    alignment=ft.MainAxisAlignment.START) if \
                    sys.platform.startswith('win32') and \
                    not self.server_flag else \
                    ft.Container(),
                # 开机自启 -------------------------------------
                ft.Row(controls=[
                    ft.Text("开机自动启动："),
                    self.sys_auto],
                    alignment=ft.MainAxisAlignment.START) if \
                    sys.platform.startswith('win32') and \
                    not self.server_flag else \
                    ft.Container(),
            ],
                alignment=ft.MainAxisAlignment.START),
            # 事件按钮 -----------------------------------------
            actions=[
                ft.TextButton("OK",
                              on_click=lambda e:
                              self.page.close(self.dlg_conf))],
            actions_alignment=ft.MainAxisAlignment.END)
        # 本地端口 ---------------------------------------------
        self.map_port = ft.TextField(
            width=110,
            hint_text="3000",
            label="本地端口",
            on_submit=self.task_created,
        )
        # 映射类型 ---------------------------------------------
        self.map_type = ft.Dropdown(
            width=100,
            label="映射类型",
            options=[
                ft.dropdown.Option("All"),
                ft.dropdown.Option("TCP"),
                ft.dropdown.Option("UDP"), ], )
        self.map_type.value = "All"

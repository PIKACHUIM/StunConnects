import random
import sys

import flet as ft
import webbrowser
import multiprocessing
from portForwards.TaskManagers import Task


class StunConnects(ft.Column):
    # 软件UI ############################################################################
    def __init__(self):
        super().__init__()
        # 全局设置 =======================================
        self.dialog = None
        self.width = 720  # 宽度
        self.tasks = ft.Column()  # 任务列表


        # 新增组件 =======================================
        # 跳转链接 ---------------------------------------
        self.map_name = ft.TextField(
            hint_text="备注名称",
            on_submit=self.add_clicked,
            width=110,
            label="备注名称",
        )
        self.dlg_name = ft.AlertDialog(
            title=ft.Text("错误"),
            content=ft.Text("请输入备注名称"),
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e: self.page.close(
                        self.dlg_name))
            ],
        )
        # 跳转链接 ---------------------------------------
        self.url_text = ft.TextField(
            hint_text="https://1web.us.kg/s/XXXXXXXX",
            on_submit=self.add_clicked,
            expand=True,
            label="跳转链接",
        )
        self.dlg_addr = ft.AlertDialog(
            title=ft.Text("错误"),
            content=ft.Text(
                "请正确填写短链接地址:\n"
                "  例如：https://1web.us.kg/p/ABCDEFGH\n"
                "  或者：https://1web.us.kg/s/ABCDEFGH\n"),
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e: self.page.close(
                        self.dlg_addr))
            ],
        )
        # 本地端口 ---------------------------------------
        self.map_port = ft.TextField(
            width=110,
            hint_text="3000",
            label="本地端口",
            on_submit=self.add_clicked,
        )

        # 映射类型 ---------------------------------------
        self.map_type = ft.Dropdown(
            width=100,
            label="映射类型",
            options=[
                ft.dropdown.Option("TCP"),
                ft.dropdown.Option("UDP"),
            ],
        )
        self.map_type.value = "TCP"

        # 过滤器 -----------------------------------------
        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="所有映射"),
                  ft.Tab(text="正在映射"),
                  ft.Tab(text="停止映射")],
        )
        # 底部 -------------------------------------------
        self.items_left = ft.Text("0个已选中")

        self.controls = [
            # 标题行 ==============================================================================
            ft.Row(
                [
                    ft.Text(value="STUN 映射助手",
                            theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            # 新增行 ==============================================================================
            ft.Row(
                controls=[
                    self.map_name,
                    self.url_text,
                    self.map_port,
                    self.map_type,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        on_click=self.add_clicked
                    ),
                ],
            ),
            # 任务列表 ============================================================================
            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.tasks,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.items_left,
                            ft.Button(
                                text="启动", on_click=None,
                                icon=ft.Icons.NOT_STARTED_ROUNDED,
                                disabled=True,
                            ),
                            ft.Button(
                                text="停止", on_click=None,
                                icon=ft.Icons.STOP_ROUNDED,
                                disabled=True,
                            ),
                            ft.Button(
                                text="删除", on_click=self.clear_clicked,
                                icon=ft.Icons.DELETE_ROUNDED,

                            ),
                            # ft.Dropdown(
                            #     width=80,
                            #     label="更新周期",
                            #     expand=True,
                            #     options=[
                            #         ft.dropdown.Option("10分钟"),
                            #         ft.dropdown.Option("30分钟"),
                            #         ft.dropdown.Option("60分钟"),
                            #     ],
                            #     border=ft.InputBorder.UNDERLINE
                            # ),
                            ft.Button(
                                text="设置",
                                on_click=None,
                                icon=ft.Icons.SETTINGS_ROUNDED,
                                disabled=True,
                            ),
                            ft.Button(
                                text="教程",
                                on_click=lambda e: webbrowser.open(
                                    "https://github.com/PIKACHUIM/StunConnects/USAGES.MD"
                                ),
                                icon=ft.Icons.BOOK_ROUNDED,
                            ),
                            ft.Button(
                                text="关于",
                                on_click=None,
                                icon=ft.Icons.INFO_ROUNDED,
                                disabled=True,
                            ),
                            ft.Button(
                                text="Github",
                                on_click=lambda e: webbrowser.open(
                                    "https://github.com/PIKACHUIM/StunConnects"
                                ),
                                icon=ft.Icons.LINK_ROUNDED,
                            ),
                        ],
                    ),
                ],
            ),
        ]

    def app_configs(self):
        pass

    def add_clicked(self, e):
        # if not self.map_name.value:
        #     self.page.open(self.dlg_name)
        #     return None
        # if not self.url_text.value \
        #         or (self.url_text.value.find("http://") < 0
        #             and self.url_text.value.find("https://") < 0):
        #     self.page.open(self.dlg_addr)
        #     return None
        if not self.map_port.value:
            self.map_port.value = random.randint(10000, 59999)
        if not self.map_type.value:
            self.map_type.value = "TCP"
        if self.url_text.value and self.map_name.value:
            task = Task(self.url_text.value,
                        self.map_name.value,
                        self.map_port.value,
                        self.map_type.value,
                        self.on_task_change,
                        self.on_task_delete)
            self.tasks.controls.append(task)
            self.map_port.value = ""
            self.map_name.value = ""
            self.url_text.value = ""
            # self.url_text.focus()
            self.update()

    def on_task_change(self, task):
        self.update()

    def on_task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.is_select:
                self.on_task_delete(task)

    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                    status == "所有映射"
                    or (status == "正在映射" and task.is_select == False)
                    or (status == "停止映射" and task.is_select)
            )
            if task.is_select:
                count += 1
        self.items_left.value = f"{count}个已选中"


def main(page: ft.Page):
    page.title = "STUN 映射助手 v0.1 Beta"
    page.fonts = {"MapleMono": "MapleMono-SC.ttf"}
    page.theme = ft.Theme(font_family="MapleMono")
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.add(StunConnects())


if __name__ == "__main__":
    multiprocessing.freeze_support()
    ft.app(main)
    # print(sys.orig_argv, sys.argv)
    # if len(sys.argv) <=1:
    #     ft.app(main)

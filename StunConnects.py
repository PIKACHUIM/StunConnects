import random
import flet as ft
from portForwards.TaskManagers import Task


class StunConnects(ft.Column):
    # 软件UI ############################################################################
    def __init__(self):
        super().__init__()
        # 全局设置 ===================================
        self.width = 700  # 宽度
        self.tasks = ft.Column()  # 任务列表

        # 新增组件 ===================================
        # 跳转链接 -----------------------------------
        self.map_name = ft.TextField(
            hint_text="备注名称",
            on_submit=self.add_clicked,
            width=100,
            label="备注名称",
        )

        # 跳转链接 -----------------------------------
        self.url_text = ft.TextField(
            hint_text="https://1web.us.kg/p/XXXXXXXX",
            on_submit=self.add_clicked,
            expand=True,
            label="跳转链接",
        )
        # 本地端口 -----------------------------------
        self.map_port = ft.TextField(
            width=100,
            hint_text="3000",
            label="本地端口",
            on_submit=self.add_clicked,
        )

        # 映射类型 -----------------------------------
        self.map_type = ft.Dropdown(
            width=80,
            label="映射类型",
            options=[
                ft.dropdown.Option("TCP"),
                ft.dropdown.Option("UDP"),
            ],
        )
        self.map_type.value = "TCP"

        # 过滤器 -------------------------------------
        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="所有映射"),
                  ft.Tab(text="正在映射"),
                  ft.Tab(text="停止映射")],
        )
        # 底部 ---------------------------------------
        self.items_left = ft.Text("0 个已映射端口")

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
                        icon=ft.icons.ADD, on_click=self.add_clicked
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
                            ft.OutlinedButton(
                                text="删除所选", on_click=self.clear_clicked
                            ),
                            ft.OutlinedButton(
                                text="关于软件", on_click=None
                            ),
                        ],
                    ),
                ],
            ),
        ]

    def app_configs(self):
        pass

    def add_clicked(self, e):
        if not self.map_port.value:
            self.map_port.value = random.randint(10000, 59999)
        if not self.map_type.value:
            self.map_type.value = "TCP"
        if self.url_text.value and self.map_name.value:
            task = Task(self.url_text.value,
                        self.map_name.value,
                        self.map_port.value,
                        self.map_type.value,
                        self.task_status_change,
                        self.task_delete)
            self.tasks.controls.append(task)
            self.map_port.value = ""
            self.map_name.value = ""
            self.url_text.value = ""
            self.url_text.focus()
            self.update()


    def task_status_change(self, task):
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)

    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                    status == "所有映射"
                    or (status == "正在映射" and task.completed == False)
                    or (status == "停止映射" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} 个已映射端口"


def main(page: ft.Page):
    page.title = "STUN 映射助手"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # create app control and add it to the page
    page.add(StunConnects())


if __name__ == "__main__":
    ft.app(main)
    # stun = StunConnects()

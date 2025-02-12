import flet as ft


class StunConnects:
    def __init__(self):
        self.page = ft.Page
        self.main = ft.app(self.main)

    def main(self, page: ft.Page):
        # page.window_width = 600  # 窗口宽度
        # page.window_height = 1200  # 窗口高度
        page.title = "STUN 自动端口转发"
        # page.vertical_alignment = ft.MainAxisAlignment.CENTER

        def add_clicked(e):
            page.add(ft.Checkbox(label=new_task.value))
            new_task.value = ""
            page.update()

        new_task = ft.TextField(hint_text="链接地址", expand=True)
        local_port = ft.TextField(hint_text="端口", expand=True)
        tasks_view = ft.Column()
        view = ft.Column(
            width=600,
            controls=[
                ft.Row(
                    controls=[
                        new_task,
                        local_port,
                        ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_clicked),
                    ],
                ),
                tasks_view,
            ],
        )

        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.add(view)


if __name__ == "__main__":
    stun = StunConnects()

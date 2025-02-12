import flet as ft


class Task(ft.Column):
    def __init__(self,
                 url_text, map_name,
                 map_port, map_type,
                 task_change,
                 task_delete
                 ):
        super().__init__()
        self.width = 700
        self.completed = False
        self.on_change = task_change
        self.on_delete = task_delete

        self.map_name = ft.Checkbox(
            width=100, value=False,
            label=map_name,
            on_change=self.status_changed
        )

        self.url_text = ft.TextField(
            expand=True,
            # label="跳转链接",
            value=url_text,
            # hint_text="https://1web.us.kg/p/XXXXXXXX",
            # border = ft.InputBorder.UNDERLINE,
            # border=ft.InputBorder.NONE,
            # read_only=True,
        )
        self.map_port = ft.TextField(
            width=150, label="本地端口",
            value="127.0.0.1:" + str(map_port),
            # border = ft.InputBorder.UNDERLINE,
            # border=ft.InputBorder.NONE,
            # read_only=True,
        )

        self.map_type = ft.Dropdown(
            width=80,
            label="映射类型",
            value=map_type,
            options=[
                ft.dropdown.Option("TCP"),
                ft.dropdown.Option("UDP"),
            ],
        )
        self.controls = [
            ft.Row(
                controls=[
                    self.map_name,
                    self.url_text,
                    self.map_port,
                    self.map_type,
                    ft.IconButton(
                        icon=ft.icons.STOP_CIRCLE_ROUNDED,
                        tooltip="Edit To-Do",
                        on_click=self.edit_clicked,
                        disabled=True,
                    ),
                    ft.IconButton(
                        ft.icons.DELETE_ROUNDED,
                        tooltip="Delete To-Do",
                        on_click=self.delete_clicked,
                        disabled=True,
                    ),
                    ft.IconButton(
                        ft.icons.EDIT_ROUNDED,
                        tooltip="Delete To-Do",
                        on_click=self.delete_clicked,
                        disabled=True,
                    ),

                ],
            )]

    def edit_clicked(self, e):
        # self.edit_name.value = self.display_task.label
        # self.display_view.visible = False
        # self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        # self.map_name.label = self.edit_name.value
        # self.display_view.visible = True
        self.update()

    def status_changed(self, e):
        self.completed = self.map_name.value
        self.on_change(self)

    def delete_clicked(self, e):
        self.on_delete(self)

import flet as ft

class StunElements:
    map_name = ft.TextField(
        hint_text="备注名称",
        on_submit=self.add_clicked,
        width=110,
        label="备注名称",
    )

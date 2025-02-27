import flet as ft


class StunGlobalUI:
    @staticmethod
    def set_ui(self):
        # UI设置 ##################################################################################
        self.controls = [
            # 标题行 ==============================================================================
            ft.Row(
                [
                    ft.Text(value="STUN 映射助手",
                            theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                alignment=ft.MainAxisAlignment.CENTER, ),
            # 新增行 ==============================================================================

            ft.Row(controls=[
                self.map_name,
                self.url_text,
            ]) if self.pages.platform == ft.PagePlatform.ANDROID else ft.Row(
                controls=[
                    self.map_name,
                    self.url_text,
                    self.url_pass,
                    self.map_port,
                    self.map_type,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        on_click=self.task_created), ],
            ),
            ft.Row(controls=[
                self.map_port,
                self.map_type,
                ft.FloatingActionButton(
                    icon=ft.Icons.ADD,
                    on_click=self.task_created),
            ]) if self.pages.platform == ft.PagePlatform.ANDROID else ft.Container(),
            # 任务列表 ============================================================================
            ft.Column(
                spacing=25, expand=True, controls=[
                    self.count,
                    self.tasks,
                    ft.Container(expand=True),
                    ft.Row(
                        controls=[
                            self.item_num, self.open_map,
                            self.demo_txt, self.demo_set,
                            self.stop_map, self.kill_map
                        ]) if self.pages.platform == ft.PagePlatform.ANDROID else \
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.item_num, self.open_map,
                                self.demo_txt, self.demo_set,
                                self.stop_map, self.kill_map,
                                self.push_set, self.push_use,
                                self.push_inf, self.push_url,
                            ]),
                    ft.Row(
                        controls=[
                            self.push_set, self.push_use,
                            self.push_inf, self.push_url
                        ]) if self.pages.platform == ft.PagePlatform.ANDROID else ft.Container(),
                ], ), ]
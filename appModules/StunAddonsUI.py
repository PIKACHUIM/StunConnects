import flet as ft

from subModules.FindResource import FindResource


class StunAddonsUI:
    @staticmethod
    def set_ui(self):
        # 新增组件 ============================================
        # 备注名称 --------------------------------------------
        self.map_name = ft.TextField(
            hint_text="备注名称",
            on_submit=self.task_created,
            width=110,
            label="备注名称")
        # 跳转链接 --------------------------------------------
        self.url_text = ft.TextField(
            hint_text="https://1web.us.kg/s/XXXXXXXX",
            on_submit=self.task_created,
            expand=True,
            label="跳转链接")
        # 需要名称 --------------------------------------------
        self.dlg_name = ft.AlertDialog(
            title=ft.Text("错误"),
            content=ft.Text("请输入备注名称"),
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e: self.page.close(
                        self.dlg_name))])
        # 映射错误 --------------------------------------------
        self.dlg_host = ft.AlertDialog(
            title=ft.Text("错误"),
            content=ft.Text(
                "请正确填写短链接地址:\n"
                "  例如：https://1web.us.kg/p/ABCDEFGH\n"
                "  或者：https://1web.us.kg/s/ABCDEFGH\n"),
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e: self.page.close(
                        self.dlg_host))])
        # 关于页面 --------------------------------------------
        self.dlg_info = ft.AlertDialog(
            title=ft.Text("关于 STUN 映射助手"),
            content=ft.Column(controls=[ft.Text(
                "------------------------------------------\n"
                "         STUN 映射助手 v0.5 Beta          \n"
                "             GPL-3.0 License              \n"
                "            作者：Pikachu Ren             \n"
                "------------------------------------------\n"
                "一个免流量和免公网转发的STUN映射自动化工具\n"
                "支持将Lucky 等工具映射的端口绑定到本地使用\n"
                "https://github.com/PIKACHUIM/StunConnects \n"
                "\n"
                "这是免费的软件，但你可以打赏作者一瓶番茄酱\n"
            ), ft.Image(
                src=FindResource.get("appSources/paids.jpg",
                                     self.server_flag),
                width=360 if not self.server_flag else 540,
                height=250 if not self.server_flag else 400,
            )
            ], alignment=ft.alignment.center), actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e:
                    self.page.close(
                        self.dlg_info))],
        )
        self.log_text = ft.TextField(
            label="日志为空",
            multiline=True,  # 多行模式
            read_only=True,  # 禁止编辑
            value="",
            expand=True,
            # width=400,  # 设置宽度
            # height=300  # 设置高度
        )
        self.log_info = ft.AlertDialog(
            title=ft.Text("运行日志"),
            content=self.log_text,
            actions=[
                ft.Row(
                    controls=[
                        ft.TextButton("清空日志", on_click=self.kill_log_dlg),
                        ft.TextButton("OK", on_click=lambda e: self.page.close(self.log_info))
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN  # 按钮对齐到两端
                )
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

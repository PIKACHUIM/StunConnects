import random
import socket
import json
import sys
import os
import flet as ft
import webbrowser
import multiprocessing

from TrayConnects import TrayConnects
from portForwards.TaskManagers import Task


class StunConnects(ft.Column):
    # 软件UI ############################################################################
    def __init__(self):
        super().__init__()
        # 全局设置 =======================================
        self.dialog = None
        self.hosts = None
        self.width = 720  # 宽度
        self.tasks = ft.Column()  # 任务列表
        self.get_local_ip()
        # 全局设置 =======================================
        self.update_time = 600
        self.server_flag = False
        self.starts_flag = False
        self.create_flag = False
        self.load_configs()
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
        # 跳转链接 ----------------------------------------
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
        self.dlg_info = ft.AlertDialog(
            title=ft.Text("关于 STUN 映射助手"),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "------------------------------------------\n"
                        "         STUN 映射助手 v0.3 Beta          \n"
                        "             GPL-3.0 License              \n"
                        "            作者：Pikachu Ren             \n"
                        "------------------------------------------\n"
                        "一个免流量和免公网转发的STUN映射自动化工具\n"
                        "支持将Lucky 等工具映射的端口绑定到本地使用\n"
                        "https://github.com/PIKACHUIM/StunConnects \n"
                        "\n"
                        "这是免费的软件，但你可以打赏作者一瓶番茄酱\n"),
                    ft.Image(
                        src="i18nLanguage/paids.jpg", width=360, height=250)
                ]),
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e:
                    self.page.close(
                        self.dlg_info))
            ],
        )
        self.sys_auto = ft.Switch(
            value=False,
            label="已禁用",
            on_change=lambda e: self.conf_startup(e),
        )
        self.sys_demo = ft.Switch(
            value=False,
            label="已禁用",
            on_change=lambda e: self.conf_service(e),
            disabled=True,
        )
        self.dlg_conf = ft.AlertDialog(
            title=ft.Text("设置"),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("自动更新周期："),
                            ft.TextField(
                                value=str(self.update_time),
                                hint_text="600",
                                text_align=ft.TextAlign.RIGHT,
                                border=ft.InputBorder.UNDERLINE,
                                width=85,
                                on_change=None,
                                disabled=True,
                            ),
                            ft.Text("秒")
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Text("查看运行日志："),
                            ft.Button(
                                text=" 查看日志",
                                icon=ft.Icons.LOGO_DEV_ROUNDED,
                                on_click=None,
                                disabled=True,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START
                    ),

                    ft.Row(
                        controls=[
                            ft.Text("作为服务安装："),
                            self.sys_demo
                        ],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    ft.Row(
                        controls=[
                            ft.Text("开机自动启动："),
                            self.sys_auto
                        ],
                        alignment=ft.MainAxisAlignment.START
                    ),
                ],
                alignment=ft.MainAxisAlignment.START
            ),
            actions=[
                ft.TextButton("保存", on_click=self.conf_changed),
                ft.TextButton("取消", on_click=lambda e:
                self.page.close(
                    self.dlg_conf))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        # 本地端口 ----------------------------------------
        self.map_port = ft.TextField(
            width=110,
            hint_text="3000",
            label="本地端口",
            on_submit=self.add_clicked,
        )

        # 映射类型 ----------------------------------------
        self.map_type = ft.Dropdown(
            width=100,
            label="映射类型",
            options=[
                ft.dropdown.Option("All"),
                ft.dropdown.Option("TCP"),
                ft.dropdown.Option("UDP"),
            ],
        )
        self.map_type.value = "All"

        # 过滤器 ------------------------------------------
        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.task_changed,
            tabs=[ft.Tab(text="所有映射"),
                  ft.Tab(text="正在映射"),
                  ft.Tab(text="停止映射")],
        )
        # 按钮 --------------------------------------------
        self.open_map = ft.Button(
            text="启动", on_click=self.task_started,
            icon=ft.Icons.NOT_STARTED_ROUNDED,
            disabled=True,
        )
        self.stop_map = ft.Button(
            text="停止", on_click=self.task_stopped,
            icon=ft.Icons.STOP_ROUNDED,
            disabled=True,
        )
        self.kill_map = ft.Button(
            text="删除", on_click=self.item_clicked,
            icon=ft.Icons.DELETE_ROUNDED,
            disabled=True,
        )
        # 底部 --------------------------------------------
        self.items_left = ft.Text("0个已选中")

        # UI设置 ##################################################################################
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
                            self.open_map,
                            self.stop_map,
                            self.kill_map,
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
                                on_click=lambda e: self.page.open(self.dlg_conf),
                                icon=ft.Icons.SETTINGS_ROUNDED,
                            ),
                            ft.Button(
                                text="教程",
                                on_click=lambda e: webbrowser.open(
                                    "https://github.com/PIKACHUIM/StunConnects/blob/main/USAGES.MD"
                                ),
                                icon=ft.Icons.BOOK_ROUNDED,
                            ),
                            ft.Button(
                                text="关于",
                                on_click=lambda e: self.page.open(self.dlg_info),
                                icon=ft.Icons.INFO_ROUNDED,
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
        self.create_flag = True

    # 新增项目 =============================================================
    def add_clicked(self, e):
        # 判定名称 ---------------------------------------------------------
        if not self.map_name.value:
            self.page.open(self.dlg_name)
            return None
        # 判定地址 ---------------------------------------------------------
        if not self.url_text.value \
                or (self.url_text.value.find("http://") < 0
                    and self.url_text.value.find("https://") < 0):
            self.page.open(self.dlg_addr)
            return None
        # 判定端口 ---------------------------------------------------------
        if not self.map_port.value:
            self.map_port.value = random.randint(10000, 59999)
        # 判定类型 ---------------------------------------------------------
        if not self.map_type.value:
            self.map_type.value = "All"
        # 执行创建 ---------------------------------------------------------
        if self.url_text.value and self.map_name.value:
            task = Task(self.url_text.value,
                        self.map_name.value,
                        self.map_port.value,
                        self.map_type.value,
                        self)
            # 清空内容 ---------------------------------
            self.tasks.controls.append(task)
            self.map_port.value = ""
            self.map_name.value = ""
            self.url_text.value = ""
            self.task_changed(None)
            self.update()

    # def task_windows(self, e):
    #     if e.data == "close":
    #         self.task_killall()

    # 全部开始 =============================================================
    def open_all_map(self):
        for task in self.tasks.controls:
            task.map_open.value = True
            task.open_clicked(None)
        self.update()

    # 全部停止 =============================================================
    def stop_all_map(self):
        for task in self.tasks.controls:
            task.map_open.value = False
            task.open_clicked(None)
        self.update()

    # 全部删除 =============================================================
    def task_killall(self):
        for task in self.tasks.controls:
            if task.map_open.value and task.ports is not None:
                task.stop_mapping()

    # 修改项目 =============================================================
    def task_started(self, e):
        for task in self.tasks.controls:
            if task.check and not task.map_open.value:
                task.map_open.value = True
                task.open_clicked(None)
                task.update()
        self.update()

    # 修改项目 =============================================================
    def task_stopped(self, e):
        for task in self.tasks.controls:
            if task.check and task.map_open.value:
                task.map_open.value = False
                task.open_clicked(None)
                task.update()
        # self.before_update()
        self.update()

    # 修改设置 =============================================================
    def conf_changed(self, e):
        if self.create_flag:
            self.save_configs()
            self.update()

    # 修改项目 =============================================================
    def task_changed(self, e):
        if self.create_flag:
            self.save_configs()
            self.update()

    # 删除项目 =============================================================
    def task_deleted(self, task):
        if self.create_flag:
            self.tasks.controls.remove(task)
            self.update()

    # 选中项目 =============================================================
    def item_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.check:
                self.task_deleted(task)

    # 内置函数 #############################################################
    # 更新之前 =============================================================
    def before_update(self):
        now_status = self.filter.tabs[self.filter.selected_index].text
        all_counts = 0
        now_counts = 0
        end_counts = 0
        for task in self.tasks.controls:
            task.visible = (
                    now_status == "所有映射"
                    or (now_status == "正在映射" and task.map_open.value)
                    or (now_status == "停止映射" and not task.map_open.value)
            )
            all_counts += 1 if task.check else 0  # 选中项目
            if task.check:
                now_counts += 0 if task.ports is None else 1  # 正在映射
                end_counts += 1 if task.ports is None else 0  # 停止映射
        # 修改按钮状态 ------------------------------------------------------
        self.items_left.value = f"{all_counts}个已选中"
        self.open_map.disabled = end_counts <= 0  # 没有已停止项目时
        self.stop_map.disabled = now_counts <= 0 or all_counts <= 0
        self.kill_map.disabled = all_counts <= 0  # 没有选中任何项目
        # print(all_counts, now_counts, end_counts)

    # 获取地址 ==============================================================
    def get_local_ip(self):
        try:
            # 创建一个UDP套接字（不连接到任何地址）
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # 连接到一个外部地址（不会真正发送数据）
            s.connect(("8.8.8.8", 80))
            # 获取本机IP地址
            self.hosts = s.getsockname()[0]
            print("Client:", "IP-" + self.hosts)
            # 关闭套接字
            s.close()
        except OSError:
            pass

    # 读取设置 ================================================================
    def load_configs(self):
        conf_path = "StunConnects.json"
        if os.path.exists(conf_path):
            with open(conf_path, "r", encoding="utf-8") as conf_file:
                conf_data = json.loads(conf_file.read())
                if "update_time" in conf_data:
                    self.update_time = conf_data["update_time"]
                if "server_flag" in conf_data:
                    self.server_flag = conf_data["server_flag"]
                if "starts_flag" in conf_data:
                    self.starts_flag = conf_data["starts_flag"]
                if "tasker_list" in conf_data:
                    for tasker_list in conf_data["tasker_list"]:
                        task = Task(
                            tasker_list['url_text'],
                            tasker_list['map_name'],
                            tasker_list['map_port'],
                            tasker_list['map_type'],
                            self,
                            tasker_list['map_flag'] \
                                if 'map_flag' in tasker_list else True)
                        task.open_clicked(None, action=False)
                        self.tasks.controls.append(task)

    # 写入设置 ================================================================
    def save_configs(self):
        conf_path = "StunConnects.json"
        with open(conf_path, "w", encoding="utf-8") as conf_file:
            conf_data = {
                "update_time": self.update_time,
                "server_flag": self.server_flag,
                "starts_flag": self.starts_flag,
                "tasker_list": [{
                    "url_text": tasker_item.url_text_data,
                    "map_name": tasker_item.map_name_data,
                    "map_port": tasker_item.map_port_data,
                    "map_type": tasker_item.map_type_data,
                    "map_flag": tasker_item.map_open.value,
                }
                    for tasker_item in self.tasks.controls
                ]
            }
            conf_file.write(json.dumps(conf_data))

    def conf_startup(self, e, app_name="Stun Connect"):
        try:
            if sys.platform.startswith('win32'):
                import winreg
                # 打开注册表项
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Run",
                    0, winreg.KEY_SET_VALUE)

                if self.sys_auto.value:
                    winreg.DeleteValue(key, app_name)
                    winreg.SetValueEx(key, app_name, 0,
                                      winreg.REG_SZ, sys.executable + " --hide-window")
                    print(f"添加启动：{sys.executable}")
                else:
                    winreg.DeleteValue(key, app_name)
                    print(f"移除启动：{sys.executable}")
                winreg.CloseKey(key)
        except FileNotFoundError:
            print(f"发生错误：启动项 {app_name} 不存在。")
        except PermissionError:
            print(f"权限不足：需要管理员权限来修改注册表")
        except Exception as e:
            print(f"发生错误：{e}")

    def conf_service(self):
        pass


# 主渲染函数 #################################################################
def main(page: ft.Page):
    # tray = None
    page.title = "STUN 映射助手 v0.3 Beta"
    page.fonts = {"MapleMono": "MapleMono-SC.ttf"}
    page.theme = ft.Theme(font_family="MapleMono")
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    view = StunConnects()
    page.window.prevent_close = True
    page.window.height = 750
    page.window.width = 750
    page.window.opacity = 0.9
    page.window.center()

    for argc in sys.argv:
        if argc.find("hide-window") >= 0:
            if sys.platform.startswith('win32'):
                page.window.always_on_top = False
                page.window_hidden = True
                page.window.skip_task_bar = True
                page.window.minimized = True

    def full_windows(e=None):
        page.window.skip_task_bar = False
        page.window_hidden = False
        page.window.focused = True
        page.window.always_on_top = True
        page.update()

    def exit_windows(e=None):
        view.task_killall()
        page.window.prevent_close = False
        page.window.close()

    def deal_windows(e):
        if e.data == "close":
            exit_windows()
        elif e.data == "minimize":
            page.window.always_on_top = False
            if sys.platform.startswith('win32'):
                page.window_hidden = True
                page.window.skip_task_bar = True
                page.update()

    tray = TrayConnects(
        full_windows,
        exit_windows,
        view.open_all_map,
        view.stop_all_map
    )
    tray.run()
    page.add(view)
    page.window.on_event = deal_windows
    page.update()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    ft.app(main)
    # print(sys.orig_argv, sys.argv)
    # if len(sys.argv) <=1:
    #     ft.app(main)

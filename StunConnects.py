import os
import sys
import flet as ft
import multiprocessing

from StunDesktops import StunDesktops
from StunServices import StunServices
from subModules.FindResource import FindResource
from multiprocessing import Process, Manager


# 主渲染函数 ###################################################################
def main(page: ft.Page):
    page.title = "STUN 映射助手 v0.5 Beta"
    file_fonts = FindResource.get("appSources/fonts.ttf")
    page.fonts = {"MapleMono": file_fonts}
    page.theme = ft.Theme(font_family="MapleMono")
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    view = StunDesktops(page, server_flag, server)
    view.load_configs()  # 加载.Conf文件
    # if view.server_flag:
    #     view.save_configs()
    page.window.prevent_close = True
    page.window.height = 750
    page.window.width = 750
    page.window.opacity = 0.95
    page.window.center()

    # 处理参数 =============================================
    for argc in sys.argv:
        if argc.find("hide-window") >= 0:
            if sys.platform.startswith('win32'):
                print("hide-window")
                page.window.always_on_top = False
                page.window_hidden = True
                page.window.skip_task_bar = True
                page.window.minimized = True

    # 打开窗口 ============================================
    def full_windows(e=None):
        page.window.skip_task_bar = False
        page.window_hidden = False
        page.window.focused = True
        page.window.always_on_top = True
        page.update()

    # 关闭窗口 ============================================
    def exit_windows(e=None):
        view.task_killall()
        page.window.prevent_close = False
        page.window.close()

    # 处理事件 ============================================
    def deal_windows(e):
        if e.data == "close":
            exit_windows()
        elif e.data == "minimize":
            page.window.always_on_top = False
            if sys.platform.startswith('win32'):
                page.window_hidden = True
                page.window.skip_task_bar = True
                page.update()

    # 设置托盘 ============================================
    if sys.platform.startswith('win32'):
        from subModules.TrayConnects import TrayConnects
        tray = TrayConnects(
            full_windows,
            exit_windows,
            view.open_all_map,
            view.stop_all_map
        )
        tray.run()
    # 启动页面 ============================================
    page.add(view)
    page.window.on_event = deal_windows
    page.update()


if __name__ == "__main__":
    # 多进程支持 ==========================================
    multiprocessing.freeze_support()
    # 启动服务 ============================================
    server_flag = False  # 本地服务模式
    server = None
    # 解析参数 ============================================
    for text in sys.argv:
        if text.find("flag-server") >= 0:
            server_flag = True
    # 本地模式 ============================================
    if server_flag:
        server = StunServices()
        client = ft.app(target=main, view=None, port=1680)
        sys.exit(0)
    ft.app(main)

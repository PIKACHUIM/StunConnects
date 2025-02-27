import random
import shutil
import socket
import json
import subprocess
import sys
import os
import time
import flet as ft

from StunServices import StunServices
from config.StunAddonsUI import StunAddonsUI
from config.StunConfigUI import StunConfigUI
from config.StunGlobalUI import StunGlobalUI
from module.FindResource import FindResource
from config.StunBottomUI import StunBottomUI
from module.TaskManagers import TaskManagers
from module.LogRecorders import Log, LL as L


class StunDesktops(ft.Column):
    # 软件UI ###############################################################
    def __init__(self, page, server_flag,
                 data: StunServices = None):
        super().__init__()
        # 全局设置 =========================

        self.count = None  # 选中任务计数int
        self.hosts = None  # 本地主机名Hosts
        self.width = 720  # 全局应用组件宽度
        self.tasks = ft.Column()  # 任务列表
        self.pages = page  # 全局页面保存API
        # 日志组件 =========================
        self.print = Log("StunConnects",
                         "StunConnects",
                         "StunConnects").log
        # 全局设置 =========================
        self.update_time = 600  # 自更新时间
        self.starts_flag = False  # 是否自启
        self.create_flag = False  # 是否完成
        self.socats_flag = False  # 外部代理
        self.server_data = data  # ServerAPI
        self.server_flag = server_flag  # CS
        self.get_local_ip()  # 获取本地Hosts
        # 控件列表 =========================
        self.controls = None  # 全局控件列表
        self.map_name = None
        self.url_text = None
        self.dlg_name = None
        self.dlg_host = None
        self.dlg_info = None
        self.open_map = None
        self.stop_map = None
        self.kill_map = None
        self.demo_run = None
        self.demo_dlg = None
        self.demo_txt = None
        self.demo_set = None
        self.item_num = None
        self.push_set = None
        self.push_use = None
        self.push_inf = None
        self.push_url = None
        self.sys_auto = None
        self.sys_demo = None
        self.set_time = None
        self.dlg_conf = None
        self.map_port = None
        self.map_type = None
        self.log_text = None
        self.log_info = None
        self.url_pass = None
        self.ext_tool = None
        self.ext_hint = None
        # 设置控件 =========================
        StunAddonsUI.set_ui(self)  # 添加GUI
        StunConfigUI.set_ui(self)  # 配置GUI
        StunBottomUI.set_ui(self)  # 底部GUI
        StunGlobalUI.set_ui(self)  # 全局GUI
        self.create_flag = True  # 初始化-OK

    # 事件函数 #############################################################
    # 清空日志 =============================================================
    def kill_log_dlg(self, e=None):
        log_file = "StunConnects.log"
        with open(log_file, "w") as log_file:
            self.page.close(self.log_info)
        self.open_log_dlg()

    # 查看日志 =============================================================
    def open_log_dlg(self, e=None):
        log_file = "StunConnects.log"
        if not os.path.exists(log_file):
            return None
        with open(log_file, "r") as log_file:
            self.log_text.value = log_file.read()
        self.page.close(self.dlg_conf)
        self.update()
        self.page.open(self.log_info)

    # 全部开始 =============================================================
    def open_all_map(self, e=None):
        for task in self.tasks.controls:
            task.map_open.value = True
            task.open_clicked(None)
        self.update()

    # 全部停止 =============================================================
    def stop_all_map(self, e=None):
        for task in self.tasks.controls:
            task.map_open.value = False
            task.open_clicked(None)
        self.update()

    # 新增项目 =============================================================
    def task_created(self, e=None):
        # 判定名称 ---------------------------------------------------------
        if not self.map_name.value:
            self.page.open(self.dlg_name)
            return None
        # 判定地址 ---------------------------------------------------------
        if not self.url_text.value \
                or (self.url_text.value.find("http://") < 0
                    and self.url_text.value.find("https://") < 0):
            self.page.open(self.dlg_host)
            return None
        # 判定端口 ---------------------------------------------------------
        if not self.map_port.value:
            self.map_port.value = random.randint(10000, 59999)
        # 判定类型 ---------------------------------------------------------
        if not self.map_type.value:
            self.map_type.value = "All"
        if self.url_pass.value:
            self.url_text.value += "?guests=" + self.url_pass.value
        # 执行创建 ---------------------------------------------------------
        if self.url_text.value and self.map_name.value:
            task = TaskManagers(
                self.url_text.value, self.map_name.value,
                self.map_port.value, self.map_type.value, self)
            # 清空内容 -----------------------------------------------------
            self.tasks.controls.append(task)
            self.map_port.value = ""
            self.map_name.value = ""
            self.url_text.value = ""
            self.url_pass.value = ""
            self.task_changed(None)
            self.update()

    # 启动项目 =============================================================
    def task_started(self, e=None):
        for task in self.tasks.controls:
            if task.check and not task.map_open.value:
                task.map_open.value = True
                task.open_clicked(None)
                task.update()
        self.update()

    # 修改项目 =============================================================
    def task_stopped(self, e=None):
        for task in self.tasks.controls:
            if task.check and task.map_open.value:
                task.map_open.value = False
                task.open_clicked(None)
                task.update()
        # self.before_update()
        self.update()

    # 全部删除 =============================================================
    def task_killall(self, e=None):
        for task in self.tasks.controls:
            if task.map_open.value and task.ports is not None:
                task.stop_mapping()

    # 修改项目 =============================================================
    def task_changed(self, e=None, save=False):
        if self.create_flag:
            if save:
                self.save_configs()
            self.update()

    # 删除项目 =============================================================
    def task_deleted(self, task):
        if self.create_flag:
            self.tasks.controls.remove(task)
            self.update()

    # 选中项目 =============================================================
    def task_clicked(self, e=None):
        for task in self.tasks.controls[:]:
            if task.check:
                self.task_deleted(task)

    # 内置函数 #############################################################
    # 更新之前 =============================================================
    def before_update(self):
        now_status = self.count.tabs[self.count.selected_index].text
        all_counts = 0
        now_counts = 0
        end_counts = 0
        for task in self.tasks.controls:
            task.visible = (
                    now_status == "所有映射" or
                    (now_status == "正在映射" and task.map_open.value) or
                    (now_status == "停止映射" and not task.map_open.value))
            all_counts += 1 if task.check else 0  # 选中项目
            if task.check:
                now_counts += 0 if task.ports is None else 1  # 正在映射
                end_counts += 1 if task.ports is None else 0  # 停止映射
        # 修改按钮状态 ------------------------------------------------------
        self.item_num.value = f"{all_counts}个已选中"
        self.open_map.disabled = end_counts <= 0  # 没有已停止项目时
        self.stop_map.disabled = now_counts <= 0 or all_counts <= 0
        self.kill_map.disabled = all_counts <= 0  # 没有选中任何项目

    # 方法函数 #############################################################
    # 获取地址 =============================================================
    def get_local_ip(self):
        LT = "get_local_ip"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 创建端口
            s.connect(("8.8.8.8", 80))  # 连接到一个外部地址
            self.hosts = s.getsockname()[0]  # 获取本机IP地址
            self.print("本地信息: LocalIP:" + self.hosts, LT, L.G)
            s.close()  # 关闭套接字
        except OSError:
            pass

    # 修改设置 =============================================================
    def conf_changed(self, e=None):
        if self.create_flag:
            self.save_configs()
            self.update()

    # 读取设置 =============================================================
    def load_configs(self):
        conf_path = "StunConnects.json"
        if not os.path.exists(conf_path):
            return None
        with open(conf_path, "r", encoding="utf-8") as conf_file:
            conf_data = json.loads(conf_file.read())
            if "update_time" in conf_data:
                self.update_time = conf_data["update_time"]
                self.set_time.value = conf_data["update_time"]
            if not self.server_flag and "server_flag" in conf_data:
                self.server_flag = conf_data["server_flag"]
                self.sys_demo.value = conf_data["server_flag"]
                self.sys_demo.label = "已启用" if self.socats_flag else "已禁用"
            if "starts_flag" in conf_data:
                self.starts_flag = conf_data["starts_flag"]
                self.sys_auto.value = conf_data["starts_flag"]
                self.sys_auto.label = "已启用" if self.socats_flag else "已禁用"
            if "socats_flag" in conf_data:
                self.socats_flag = conf_data["socats_flag"]
                self.ext_tool.value = conf_data["socats_flag"]
                self.ext_tool.label = "已启用" if self.socats_flag else "已禁用"
            if "tasker_list" in conf_data:
                for tasker_list in conf_data["tasker_list"]:
                    task = TaskManagers(
                        tasker_list['url_text'],
                        tasker_list['map_name'],
                        tasker_list['map_port'],
                        tasker_list['map_type'],
                        self,
                        tasker_list['map_flag'] \
                            if 'map_flag' in tasker_list else True,
                        now_open=False)
                    task.open_clicked(None, action=False)
                    self.tasks.controls.append(task)

    # 写入设置 =============================================================
    def save_configs(self, e=None):
        conf_path = "StunConnects.json"
        with open(conf_path, "w", encoding="utf-8") as conf_file:
            conf_data = {
                "update_time": self.update_time,
                "server_flag": self.server_flag,
                "starts_flag": self.starts_flag,
                "socats_flag": self.socats_flag,
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
            # self.print("保存设置: " + json.dumps(conf_data))
            conf_file.write(json.dumps(conf_data))
        # 重载服务 =========================================================
        # print("save_configs", self.server_flag, self.server_data)
        # traceback.print_stack(sys._getframe())
        if self.server_flag and self.server_data:
            self.server_data.load()

    # 自动启动 =============================================================
    def config_socat(self, e):
        self.socats_flag = self.ext_tool.value
        self.ext_tool.label = "已启用" if self.socats_flag else "已禁用"
        self.ext_hint = ft.AlertDialog(
            title=ft.Text("提示"),
            content=ft.Text("切换Socat将会在重启后生效"),
            actions=[
                ft.TextButton(
                    "OK",
                    on_click=lambda e: self.page.close(self.ext_hint))])
        self.page.open(self.ext_hint)
        self.save_configs()
        self.update()

    # 自动启动 =============================================================
    def conf_startup(self, e, app_name="Stun Connect"):
        LT = "conf_startup"
        try:  # 控制启动状态 ===============================================
            self.starts_flag = self.sys_auto.value  # 同步变量 -------------
            self.sys_auto.label = "已启用" if self.starts_flag else "已禁用"
            self.update()
            self.page.close(self.dlg_conf)
            self.page.open(self.dlg_conf)
            if sys.platform.startswith('win32'):  # Windows系统 ------------
                import winreg
                # 打开注册表项 ---------------------------------------------
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Run",
                    0, winreg.KEY_SET_VALUE)
                if self.sys_auto.value:
                    try:  # 删除启动项 --------------------------------------
                        winreg.DeleteValue(key, app_name)  # 删除启动项 -----
                    except (FileNotFoundError, Exception):  # 捕获异常 ------
                        pass  # 不存在则忽略 --------------------------------
                    winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ,
                                      sys.executable + " --hide-window")
                    self.print(f"添加启动：{sys.executable}", LT, L.G)
                else:  # 删除启动项 -----------------------------------------
                    winreg.DeleteValue(key, app_name)
                    self.print(f"移除启动：{sys.executable}", LT, L.G)
                winreg.CloseKey(key)
                self.save_configs()
        except FileNotFoundError:
            self.print(f"发生错误：启动项 {app_name} 不存在。", LT, L.W_)
        except PermissionError:
            self.print(f"权限不足：需要管理员权限来修改注册表", LT, L.E_)
        except Exception as e:
            self.print(f"发生错误：{e}", LT, L.E_)

    # 服务设置 =============================================================
    def flag_service(self, e=None, f=None):
        if f is None:
            f = self.sys_demo.value
        if f:
            self.nssm_control("start StunConnects")
        else:
            self.nssm_control("stop StunConnects")

    # 服务重启 =============================================================
    def load_service(self, e=None):
        self.flag_service(f=False)
        self.save_configs()
        time.sleep(5)
        self.flag_service(f=True)

    # 服务控制 =============================================================
    def nssm_control(self, action, nssm_path=None):
        LT = "nssm_control"
        self.print("服务控制: " + action, LT, L.G)
        if nssm_path is None:
            nssm_path = FindResource.get("assets/tools.exe")
        nssm_data = subprocess.run(nssm_path + " " + action,
                                   shell=True, capture_output=True)
        nssm_text = (nssm_data.stdout + nssm_data.stderr).decode("utf-16")
        nssm_text = nssm_text.replace("\n", "").replace("\r", "")
        self.print("执行结果: " + nssm_text, LT, L.M)

    # 服务安装 =============================================================
    def conf_service(self, e=None):
        LT = "conf_service"
        self.server_flag = self.sys_demo.value
        self.sys_demo.label = "已启用" if self.server_flag else "已禁用"
        self.save_configs()
        self.update()
        self.page.close(self.dlg_conf)
        self.page.open(self.dlg_conf)
        # 获取路径 ==============================================
        data_path = os.environ.get('APPDATA')
        nssm_path = FindResource.get("assets/tools.exe")
        if self.server_flag:  # 设置服务 ========================
            try:
                shutil.copy(nssm_path, data_path)
                nssm_path = os.path.join(data_path, "tools.exe")
            except (FileNotFoundError, Exception) as err:
                self.print("创建服务失败: " + str(err), LT, L.W_)
            # 设置环境变量 ======================================
            start_cmd = os.getcwd() + "/StunConnects.exe"
            setup_cmd = "install StunConnects \"%s\"" % start_cmd
            setup_dir = "AppDirectory \"%s\"" % os.getcwd()
            setup_dir = "set StunConnects %s" % setup_dir
            setup_app = "AppParameters \"--flag-server\""
            setup_app = "set StunConnects %s" % setup_app
            start_app = "start StunConnects"
            # 设置服务 ==========================================
            self.nssm_control(setup_cmd, nssm_path)
            self.nssm_control(setup_dir, nssm_path)
            self.nssm_control(setup_app, nssm_path)
            self.nssm_control(start_app, nssm_path)
            # 设置界面 ==========================================
            self.sys_auto.value = False
            self.sys_demo.label = "已启用"
            self.open_map.visible = False
            self.stop_map.visible = False
            self.kill_map.visible = False
            self.demo_set.visible = True
            self.demo_txt.visible = True
            # 设置任务 ==========================================
            if self.starts_flag:
                self.conf_startup(None)
            for task_now in self.tasks.controls:
                if task_now.ports is not None:
                    task_now.stop_mapping()
        else:  # 删除服务 =======================================
            setup_app = "remove StunConnects confirm"
            self.nssm_control("stop StunConnects", nssm_path)
            self.nssm_control(setup_app, nssm_path)
            # 设置界面 ==========================================
            self.sys_demo.label = "已禁用"
            self.open_map.visible = True
            self.stop_map.visible = True
            self.kill_map.visible = True
            self.demo_set.visible = False
            self.demo_txt.visible = False
            # 设置任务 ==========================================
            for task_now in self.tasks.controls:
                if task_now.ports is not None:
                    task_now.open_mapping()
        # 保存设置 ==============================================
        self.update()

import json
import os
import sys
import threading
import time
import traceback

from subModules.LogRecorders import Log, LL as L
from subModules.AllForwarder import PortForwards


class StunServices(threading.Thread):
    def __init__(self, set_time=600):
        super().__init__()
        # 创建数据 ===================
        self.map_list = {}  # 映射列表
        self.put_time = time.time()
        self.set_time = set_time
        self.api_logs = Log(
            "StunConnects",
            "StunConnects",
            "StunConnects"
        ).log
        # 启动线程 ===================
        self.start()

    # 启动线程 =======================
    def run(self):
        self.open()

    # 服务内容 =========================================================
    def open(self):
        self.load()
        # for task_name in self.map_list:
        #     try:
        #         self.map_list[task_name].join()
        #     except (RuntimeError, Exception):
        #         continue

    # 结束服务 =========================================================
    def stop(self):
        for task_name in self.map_list:
            self.map_list[task_name].kill()

    # 载入数据 =========================================================
    def load(self):
        conf_path = "StunConnects.json"
        if not os.path.exists(conf_path):
            return False
        with open(conf_path, "r", encoding="utf-8") as conf_file:
            conf_data = json.loads(conf_file.read())
            if "update_time" in conf_data:
                self.set_time = conf_data["update_time"]
            if "tasker_list" in conf_data:
                for task_now in conf_data["tasker_list"]:
                    # print(task_now)
                    self.deal(task_now)

    # 处理变更 =========================================================
    def deal(self, task_dict):
        url_text = task_dict['url_text']
        # 新增任务 ==============================
        if url_text not in self.map_list:
            # 任务启用 ==========================
            if task_dict['map_flag']:
                self.api_logs("新增任务: " + url_text)
                self.task(task_dict)
                return True
        else:
            old_task = self.map_list[url_text]
            # 停止并删除当前
            if not task_dict['map_flag']:
                self.api_logs("停止任务: " + url_text)
                old_task.kill()
                self.map_list.pop(url_text)
                return False
            elif int(old_task.local_port) != int(task_dict['map_port']) \
                    or old_task.proxy_urls != url_text \
                    or old_task.time != self.set_time \
                    or old_task.proxy_type != task_dict['map_type']:
                # print(int(old_task.local_port) != int(task_dict['map_port']))
                # print(old_task.proxy_urls != url_text)
                # print(old_task.time != self.set_time, old_task.time, self.set_time)
                # print(old_task.proxy_type != task_dict['map_type'])
                self.api_logs("任务变更: " + url_text)
                # traceback.print_stack(sys._getframe())
                old_task.kill()
                self.task(task_dict)
                return True
            else:
                self.api_logs("暂无变更: " + url_text)
                return True

    # 新增任务 =========================================================
    def task(self, task_dict):
        url_text = task_dict['url_text']
        if not task_dict['map_flag']:
            return False
        map_task = PortForwards(
            task_dict['map_port'],
            "0.0.0.0",
            proxy_type=task_dict['map_type'],
            proxy_urls=url_text,
            server_tip="StunConnects",
            in_dog_var = self.set_time
        )
        self.map_list[url_text] = map_task
        map_task.start()


if __name__ == '__main__':
    stu = StunServices()

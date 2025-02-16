import json
import os
import time
from subModules.AllForwarder import PortForwards

class StunServices():
    def __init__(self):
        self.map_list = []
        self.set_time = 600

    def run(self):
        self.open()

    # 服务内容 =========================================================
    def open(self):
        conf_path = "StunConnects.json"
        if os.path.exists(conf_path):
            with open(conf_path, "r", encoding="utf-8") as conf_file:
                conf_data = json.loads(conf_file.read())
                if "update_time" in conf_data:
                    self.set_time = conf_data["update_time"]
                if "tasker_list" in conf_data:
                    for tasker_list in conf_data["tasker_list"]:
                        self.map_list.append(
                            PortForwards(
                                tasker_list['map_port'],
                                "0.0.0.0",
                                proxy_type=tasker_list['map_type'],
                                proxy_urls=tasker_list['url_text']))
                        self.map_list[-1].start()
        for tasker_item in self.map_list:
            tasker_item.join()

    # 结束服务 =========================================================
    def stop(self):
        for tasker_item in self.map_list:
            tasker_item.kill()


if __name__ == '__main__':
    stu = StunServices()

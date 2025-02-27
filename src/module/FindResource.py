import os
import sys


class FindResource:
    @staticmethod
    def get(relative_path, server_flag=False):
        if server_flag:
            return "https://123pan.pika.net.cn/Mirrors/app/StunConnects/" + relative_path
        if hasattr(sys, '_MEIPASS'):  # 如果是打包后的程序
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath(""), relative_path)

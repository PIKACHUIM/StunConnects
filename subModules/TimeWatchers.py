import threading
import time


class TimeWatchers(threading.Thread):
    def __init__(self, in_task, in_time=600):
        super().__init__()
        self.task = in_task
        self.time = in_time
        self.flag = True
        self.last = time.time()

    def run(self):
        while self.flag:
            if time.time() - self.last >= self.time:
                for task_now in self.task:
                    if task_now.ports is not None:
                        task_now.ports.set()
                self.last = time.time()
            time.sleep(1)

class PortWatchers(threading.Thread):
    def __init__(self,
                 in_main,
                 in_time=600,
                 in_logs=None):
        super().__init__()
        self.main = in_main
        self.time = in_time
        self.flag = True
        self.logs = in_logs
        self.last = time.time()

    def run(self):
        while self.flag:
            if time.time() - self.last >= self.time:
                self.main.set()
                self.last = time.time()
                self.logs("Update: Check URL Change")
            time.sleep(1)

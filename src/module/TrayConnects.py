import threading
import pystray
from PIL import Image
from pystray import MenuItem

from src.module.FindResource import FindResource


class TrayConnects():
    def __init__(self,
                 in_full,
                 in_exit,
                 in_open,
                 in_stop):
        # super().__init__()
        self.in_full = in_full
        self.in_exit = in_exit
        self.in_open = in_open
        self.in_stop = in_stop
        self.proc = None
        self.menu = (
            MenuItem('全部开始', self.in_open),
            MenuItem('全部停止', self.in_stop),
            pystray.Menu.SEPARATOR,
            MenuItem('打开', self.set),
            MenuItem('退出', self.end)
        )
        self.icon = Image.open(FindResource.get("assets/icons.png"))
        self.tray = pystray.Icon("STUN 映射助手", self.icon,
                                 "STUN 映射助手", self.menu)

    def run(self):
        self.proc = threading.Thread(target=self.tray.run, daemon=True)
        self.proc.start()

    def set(self):
        # self.tray.stop()
        self.in_full()

    def end(self):
        self.tray.stop()
        self.in_exit()

if __name__ == '__main__':
    tray = TrayConnects()

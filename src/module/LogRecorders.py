# -*- coding: utf-8 -*-
# --------------------------------------------------------
#                      日志输出模块
# --------------------------------------------------------
import os
import sys
import time
import traceback
from enum import Enum

texts = ["调试", "成功", "信息",
         "警告", "错误", "严重",
         "提醒",
         "调试", "成功", "信息",
         "警告", "错误", "严重",
         "提醒", ]
color = ["0;37;40m", "1;32;40m", "1;34;40m",
         "1;33;40m", "1;35;40m", "1;31;40m",
         "1;36;40m",
         "1;30;47m", "1;30;42m", "1;30;44m",
         "1;30;43m", "1;30;45m", "1;33;41m",
         "1;30;46m", ]


# 枚举类 -------------------------------------------------
class LogLevel(Enum):
    D = DEBUG = Debug = debug = 0
    S = SUCCESS = Success = success = 1
    M = MESSAGE = Message = message = 2
    W = WARNING = Warning = warning = 3
    E = ERROR = Error = error = 4
    F = FATAL = Fatal = fatal = 5
    G = GREAT = Great = great = 6
    D_ = DEBUG_ = Debug_ = debug_ = 7
    S_ = SUCCESS_ = Success_ = success_ = 8
    M_ = MESSAGE_ = Message_ = message_ = 9
    W_ = WARNING_ = Warning_ = warning_ = 10
    E_ = ERROR_ = Error_ = error_ = 11
    F_ = FATAL_ = Fatal_ = fatal_ = 12
    G_ = GREAT_ = Great_ = great_ = 13
    LONGS = ("-----------------------------------------"
             "-----------------------------------------"
             "----------------")

    @staticmethod
    # 生成字符串 -----------------------------------------
    def str(in_level, is_color=True):
        if is_color:
            return "\033[" \
                + color[in_level.value] + "[" \
                + texts[in_level.value] + "]\033[0m"
        else:
            return "[" + texts[in_level.value] + "]"

    def __str__(self):
        return LogLevel.str(self)


# 枚举类别名 ---------------------------------------------
LL = LEVEL = level = ll = LOG_LEVEL = log_level = LogLevel
MIN_OUT_LEVEL = LogLevel.debug
stamps_time = time.strftime("%m%d-%H%M%S",
                            time.localtime())


class Log:
    # 构造方法 -------------------------------------------
    def __init__(self,
                 main_name: str = "Undefined",  # 主要名称
                 mods_name: str = "Undefined",  # 模块名称
                 exec_name: str = "Undefined",  # 函数名称
                 sub_files: [str, None] = "log",  # 后缀名
                 max_lines: [int, bool] = 92.00,  # 单行长
                 out_paths: [str, None] = ".",  # 保存路径
                 out_lines: bool = True,  # 启用行编号输出
                 ):
        # 初始化模块 -------------------------------------
        self.split_l = out_lines
        self.print_l = max_lines
        self.masters = main_name[:12]
        self.modules = mods_name[:12]
        self.execute = exec_name[:12]
        self.o_file = "%s/%s.%s" % (
            out_paths, main_name, sub_files)

    # 输出日志 ------------------------------------------
    def log(self,
            # 消息内容 ----------------------------------
            in_texts: [str] = LL.LONGS.value,
            # 重写函数名称，函数内部会使用 --------------
            in_master: [str, None] = None,
            # 消息等级和颜色：LogLevel:0~5 --------------
            in_level: LL = LogLevel.DEBUG,
            # 消息显示的颜色，可以和等级不同 ------------
            in_color: [int, LL, None] = None):
        # 输出日志 ======================================
        # 判断类型 --------------------------------------
        c_level = n_level = in_level
        if type(in_level) is not str:
            c_level = LogLevel.str(in_level)
            n_level = LogLevel.str(in_level, False)
        # 重写模块 -----------------------------------
        if in_color is None:
            in_color: LogLevel = in_level
        if in_master is None:
            in_master = self.execute
        if type(in_level) is LogLevel:
            if in_level.value < MIN_OUT_LEVEL.value:
                return None
        # 准备数据 ------------------------------------------------------------------------
        in_master = in_master
        in_module = self.masters
        in_thread = self.modules
        timer = time.strftime("%m-%d %H:%M:%S", time.localtime())
        c_str = "\033[1;37;40m[" + timer + "]\033[0m"
        c_str = c_str + "\033[1;37;40m[" + "%-10s" % in_thread.center(10) + "]\033[0m"
        c_str = c_str + "\033[1;37;40m[" + "%-10s" % in_module.center(10) + "]\033[0m"
        c_str = c_str + "\033[1;37;40m[" + "%-8s" % in_master.center(11) + "]\033[0m"
        n_str = c_str.replace(c_level, str(n_level))
        n_str = n_str.replace("\033[1;37;40m[", "[").replace("]\033[0m", "]")
        c_str = c_str + c_level
        c_str = c_str + "\033[" + color[int(in_color.value)] + in_texts + "\033[0m"
        n_str = n_str + in_texts
        print(c_str)
        # 写入文件 -----------------------------------------------------------------------
        if self.o_file is not None:
            with open(self.o_file, 'a+') as out_file:
                out_file.write(n_str + "\n")
        if in_level.value in [LL.E.value, LL.E_.value, LL.F.value, LL.F_.value]:
            traceback.print_exc()
        # --------------------------------------------------------------------------------

    def ptr(self,
            # 重写函数名称，函数内部会使用 --------------
            in_funcs: [str, None] = None,
            # 消息等级和颜色：LogLevel:0~5 --------------
            in_level: [str, LogLevel] = LogLevel.Message,
            # 消息显示的颜色，可以和等级不同 ------------
            in_color: [int, LogLevel] = LogLevel.Debug):
        # 获取路径并输出 -----------------------------------------
        lp = sys._getframe().f_lineno
        fp = sys._getframe().f_code.co_filename
        self.log("位置: " + str(lp), in_level, in_color, in_funcs)
        self.log("文件: " + str(fp), in_level, in_color, in_funcs)

    def cut(self, length=58):
        string = ""
        while length > 0:
            string += '-'
        self.log(string)


if __name__ == '__main__':
    logger_test = Log("测试线程", "模块名称", "函数名称")
    logger_test.log("DEBUG", in_level=LogLevel.DEBUG)
    logger_test.log("SUCCESS", in_level=LogLevel.SUCCESS)
    logger_test.log("MESSAGE", in_level=LogLevel.MESSAGE)
    logger_test.log("WARNING", in_level=LogLevel.WARNING)
    logger_test.log("ERROR", in_level=LogLevel.ERROR)
    logger_test.log("FATAL", in_level=LogLevel.FATAL)
    logger_test.log("DEBUG", in_level=LogLevel.DEBUG, backFlag=True)
    logger_test.log("SUCCESS", in_level=LogLevel.SUCCESS, backFlag=True)
    logger_test.log("MESSAGE", in_level=LogLevel.MESSAGE, backFlag=True)
    logger_test.log("WARNING", in_level=LogLevel.WARNING, backFlag=True)
    logger_test.log("ERROR", in_level=LogLevel.ERROR, backFlag=True)
    logger_test.log("FATAL", in_level=LogLevel.FATAL, backFlag=True)
    logger_test.log("great", in_level=LogLevel.great)
    logger_test.log("great", in_level=LogLevel.great, backFlag=True)

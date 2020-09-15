# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2020/5/9 20:22 
  @Auth : 可优
  @File : handle_log.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
import os
import logging

from scripts.handle_yaml import do_yaml
from scripts.handle_path import LOG_PATH


class HandleLog:

    def __init__(self, name=None):
        # 1、创建Logger对象
        # 相当于日志记录工具
        if name is None:
            self.my_logger = logging.getLogger("testcase")
        else:
            self.my_logger = logging.getLogger(name)

        # 2、设置日志器的日志等级
        # self.my_logger.setLevel("DEBUG")
        self.my_logger.setLevel(do_yaml.get_data("log", "logger_level"))

        # 3、创建日志输出渠道（日志显示的地方）
        console_handler = logging.StreamHandler()
        console_handler.setLevel("WARNING")

        # file_handler = logging.FileHandler("testcase.log", encoding="utf-8")
        # file_handler = logging.FileHandler(do_yaml.get_data("log", "log_filename"), encoding="utf-8")
        log_full_path = os.path.join(LOG_PATH, do_yaml.get_data("log", "log_filename"))
        file_handler = logging.FileHandler(log_full_path, encoding="utf-8")

        # 4、创建日志的显示样式（格式）并与渠道进行关联
        formater = logging.Formatter('%(asctime)s - [%(levelname)s] - [msg]: %(message)s - %(name)s - %(lineno)d')
        console_handler.setFormatter(formater)
        file_handler.setFormatter(formater)

        # 5、日志器对象与日志输出渠道（展示的地方）进行关联
        self.my_logger.addHandler(console_handler)
        self.my_logger.addHandler(file_handler)

    def get_logger(self):
        return self.my_logger


do_log = HandleLog().get_logger()

if __name__ == '__main__':
    do_log = HandleLog()
    my_logger = do_log.get_logger()
    my_logger.debug("这是一条debug级别的日志！")
    my_logger.info("这是一条info级别的日志！")
    my_logger.warning("这是一条warning级别的日志！")
    my_logger.error("这是一条error级别的日志！")
    my_logger.critical("这是一条critical级别的日志！")

# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2020/4/29 21:22 
  @Auth : 可优
  @File : lm_03_unittest_report.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
import os
from datetime import datetime

import unittest

# print(1/0)
# from HTMLTestRunnerNew import HTMLTestRunner
from libs.HTMLTestRunnerNew import HTMLTestRunner
# from handle_yaml import do_yaml
from scripts.handle_yaml import do_yaml
from scripts.handle_path import CASES_PATH, REPORTS_PATH
from scripts.handle_user import generate_three_user

# 在执行用例之后，先创建三个用户并存放在全局数据池GlobalData中
# generate_three_user()

# suite = unittest.defaultTestLoader.discover(r"C:\Users\KeYou\PycharmProjects\TestApi0509\cases")
suite = unittest.defaultTestLoader.discover(CASES_PATH)

# html_filename = do_yaml.get_data("report", "filename")
# html_filename = r"C:\Users\KeYou\PycharmProjects\TestApi0509\reports" + "\\" + html_filename
# html_filename = os.path.join(REPORTS_PATH, html_filename)

html_filename = do_yaml.get_data('report', 'filename') + '_' + datetime.strftime(datetime.now(), "%Y%m%d%H%M%S") + ".html"
html_filename = os.path.join(REPORTS_PATH, html_filename)

with open(html_filename, "wb") as file:
    runner = HTMLTestRunner(file,
                            verbosity=do_yaml.get_data("report", "verbosity"),
                            title=do_yaml.get_data("report", "title"),
                            description=do_yaml.get_data("report", "description"),
                            tester=do_yaml.get_data("report", "tester"))
    runner.run(suite)

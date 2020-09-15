# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2020/4/27 20:35 
  @Auth : 可优
  @File : lm_02_unittest_define.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
import unittest

# import ddt
from libs import ddt

from scripts.handle_request import HandleRequest
from scripts.handle_excel import HandleExcel
from scripts.handle_yaml import do_yaml
from scripts.handle_log import do_log
from scripts.handle_mysql import HandleMysql
from scripts.handle_parameterize import GlobalData, Parameterize


@ddt.ddt
class TestRegister(unittest.TestCase):
    do_excel = HandleExcel(do_yaml.get_data("excel", "filename"), "register")
    testcases_data = do_excel.read_data()  # 嵌套用例对象的列表

    @classmethod
    def setUpClass(cls):
        cls.do_request = HandleRequest()
        cls.do_request.add_headers(do_yaml.get_data("api", "api_version"))

        cls.do_mysql = HandleMysql()
        # cls.do_mysql.create_not_existed_mobile()
        do_log.info("开始执行用例")

    @classmethod
    def tearDownClass(cls):
        cls.do_request.close()
        cls.do_mysql.close()
        do_log.info("用例执行结束")

    @ddt.data(*testcases_data)
    def test_register(self, one_testcase):
        # 在每条用例执行之前，获取未注册的手机号码，然后更新全局数据池
        setattr(GlobalData, "${not_existed_tel}", self.do_mysql.create_not_existed_mobile())

        # 将excel中读取的请求参数进行参数化
        new_data = Parameterize.to_parma(one_testcase.data)

        new_url = do_yaml.get_data("api", "base_url") + one_testcase.url
        res = self.do_request.send(one_testcase.method,
                                   new_url,
                                   json=new_data)

        real_code = res.json()["code"]
        # row = testcase_dict["id"] + 1
        # self.do_excel.write_data(row, 7, res.text)
        # name = testcase_dict["name"]
        try:
            self.assertEqual(one_testcase.expected_value,
                             real_code,
                             one_testcase.name)
        except AssertionError as e:
            # print("此处需要使用日志器来记录日志！")
            # my_logger.error(f"{one_testcase.name}：具体异常为{e}")
            do_log.error(f"{one_testcase.name}：具体异常为{e}")
            # print(f"具体异常为：{e}")
            # self.do_excel.write_data(row, 8, "失败")
            self.do_excel.write_data(one_testcase, res.text, "失败")
            raise e
        else:
            # self.do_excel.write_data(row, 8, "成功")
            # do_log.debug(res.text)
            self.do_excel.write_data(one_testcase, res.text, "成功")


if __name__ == '__main__':
    unittest.main()

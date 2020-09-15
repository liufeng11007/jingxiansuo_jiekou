import json
import unittest

from libs import ddt
from scripts.handle_request import HandleRequest
from scripts.handle_excel import HandleExcel
from scripts.handle_yaml import do_yaml
from scripts.handle_log import do_log
from scripts.handle_mysql import HandleMysql
from scripts.handle_parameterize import Parameterize, GlobalData


@ddt.ddt
class TestRecharge(unittest.TestCase):
    do_excel = HandleExcel(do_yaml.get_data("excel", "filename"), "recharge")
    testcases_data = do_excel.read_data()  # 嵌套字典的列表

    @classmethod
    def setUpClass(cls):
        # 创建HandleRequest对象
        cls.do_request = HandleRequest()
        # 获取url版本请求头数据并添加至请求头中
        cls.do_request.add_headers(do_yaml.get_data("api", "api_version"))
        # 创建HandleMysql对象
        cls.do_mysql = HandleMysql()

        # 创建一个不存在的用户id，并加入到全局数据池中
        setattr(GlobalData, "${not_existed_id}", cls.do_mysql.get_not_existed_user_id())

        do_log.info("开始执行用例")

    @classmethod
    def tearDownClass(cls):
        cls.do_request.close()
        # 关闭连接
        cls.do_mysql.close()
        do_log.info("用例执行结束")

    @ddt.data(*testcases_data)
    def test_recharge(self, one_testcase):
        new_data = Parameterize.to_parma(one_testcase.data)

        new_url = do_yaml.get_data("api", "base_url") + one_testcase.url
        # 1、在充值之前，查询当前用例的金额
        # 在发起请求之前, 查询当前账户金额
        check_sql = one_testcase.check_sql
        if check_sql:
            check_sql = Parameterize.to_parma(check_sql)
            mysql_data = self.do_mysql.get_one_value(sql=check_sql)
            amount_before = float(mysql_data['leave_amount'])  # 不是float浮点数, 也不是int类型, 是decimal数据类型

        # 2、进行充值
        res = self.do_request.send(one_testcase.method,
                                   new_url,
                                   json=new_data)

        # 获取响应数据并转化为字典类型
        actual_value = res.json()
        try:
            # one_testcase.expected_value为int类型，需要转化为字符串类型
            # self.assertIn(one_testcase.expected_value,
            #               res.text,
            #               one_testcase.name)
            self.assertEqual(one_testcase.expected_value,
                             actual_value.get("code"),
                             one_testcase.name)
            # 3、查询充值成功之后的金额
            # 如果check_sql不为空, 说明要进行数据校验
            if check_sql:
                mysql_data = self.do_mysql.get_one_value(sql=check_sql)
                amount_after = float(mysql_data['leave_amount'])

                one_dict = json.loads(new_data, encoding='utf-8')
                currrent_recharge_amount = one_dict['amount']

                actual_amount = amount_before + currrent_recharge_amount
                self.assertEqual(actual_amount, amount_after, msg="数据库中充值的金额有误")
        except AssertionError as e:
            do_log.error(f"{one_testcase.name}：具体异常为{e}")
            self.do_excel.write_data(one_testcase, res.text, "失败")
            raise e
        else:
            # if one_testcase.id == 2:
            # a.如果响应报文中含有token_info，说明当前用例为登录接口用例
            # b.从响应报文中获取token，然后添加至请求头中
            if "token_info" in res.text:
                token = actual_value["data"]["token_info"]["token"]

                # add_headers需要传字典类型
                # self.do_request.add_headers("Authorization", f"Bearer {token}")
                headers = {"Authorization": "Bearer " + token}
                self.do_request.add_headers(headers)
            self.do_excel.write_data(one_testcase, res.text, "成功")


if __name__ == '__main__':
    unittest.main()

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
class TestInvest(unittest.TestCase):
    """
    投资接口测试类
    """
    do_excel = HandleExcel(do_yaml.get_data("excel", "filename"), "invest")
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
        # 创建一个不存在的loan id，并加入到全局数据池中
        setattr(GlobalData, "${not_existed_loan_id}", cls.do_mysql.get_not_existed_loan_id())

        do_log.info("开始执行用例")

    @classmethod
    def tearDownClass(cls):
        cls.do_request.close()
        # 关闭连接
        cls.do_mysql.close()
        do_log.info("用例执行结束")

    @ddt.data(*testcases_data)
    def test_invest(self, one_testcase):
        new_data = Parameterize.to_parma(one_testcase.data)

        new_url = do_yaml.get_data("api", "base_url") + one_testcase.url

        # 进行加标
        res = self.do_request.send(one_testcase.method,
                                   new_url,
                                   json=new_data)

        # 获取响应数据并转化为字典类型
        actual_value = res.json()
        try:
            self.assertEqual(one_testcase.expected_value,
                             actual_value.get("code"),
                             one_testcase.name)
        except AssertionError as e:
            do_log.error(f"{one_testcase.name}：具体异常为{e}")
            self.do_excel.write_data(one_testcase, res.text, "失败")
            raise e
        else:
            # if one_testcase.id == 2:
            # a.如果响应报文中含有token_info，说明当前用例为登录接口用例
            # b.从响应报文中获取token，然后添加至请求头中
            if "token_info" in res.text:
                token = res.json()["data"]["token_info"]["token"]
                # add_headers需要传字典类型
                headers = {"Authorization": "Bearer " + token}
                self.do_request.add_headers(headers)

            check_sql_str = one_testcase.check_sql
            if check_sql_str:
                # 将check_sql json格式的字符串转化为字典
                check_sql_dict = json.loads(check_sql_str, encoding='utf-8')
                if 'loan_id' in check_sql_dict:
                    # 获取查询loan id的sql语句
                    loan_id_sql = check_sql_dict.get('loan_id')
                    # 将sql语句进行参数化
                    loan_id_sql = Parameterize.to_parma(loan_id_sql)
                    mysql_data = self.do_mysql.get_one_value(sql=loan_id_sql)

                    load_id = mysql_data['id']  # 获取loan_id
                    # 设置loan_id为GlobalData的类属性
                    setattr(GlobalData, '${loan_id}', load_id)

            self.do_excel.write_data(one_testcase, res.text, "成功")


if __name__ == '__main__':
    unittest.main()

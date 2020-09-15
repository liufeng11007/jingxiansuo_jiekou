# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2020/5/11 20:29 
  @Auth : 可优
  @File : handle_user.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
from scripts.handle_request import HandleRequest
from scripts.handle_mysql import HandleMysql
from scripts.handle_yaml import do_yaml
from scripts.handle_parameterize import GlobalData


def create_user(reg_name, password=12345678, type=1):
    """
    创建用户并将用户信息，添加至全局数据池中
    :param reg_name: 用户昵称
    :param password: 用户密码，默认为12345678
    :param type: 用户类型，默认为1，普通用户
    :return:
    """
    do_request = HandleRequest()
    do_mysql = HandleMysql()

    # 获取未注册手机号
    mobile_phone = do_mysql.create_not_existed_mobile()
    # 构造请求参数
    param = {
        "mobile_phone": mobile_phone,
        "pwd": password,
        "reg_name": reg_name,
        "type": type
    }
    # 构造请求url路径
    url = "http://api.lemonban.com/futureloan/member/register"
    # 获取api头信息
    do_request.add_headers(do_yaml.get_data("api", "api_version"))

    # 进行注册
    res = do_request.send("POST", url, json=param)

    # sql = do_yaml.get_data("mysql", "select_user_sql")
    # do_mysql.get_values(sql, )
    # 从响应报文中获取用户id
    user_id = res.json()["data"]["id"]

    # 关闭相关连接
    do_request.close()
    do_mysql.close()

    # 将用户信息添加至全局数据池中
    setattr(GlobalData, "${" + reg_name + "_user_tel}", mobile_phone)
    setattr(GlobalData, "${" + reg_name + "_user_pwd}", password)
    setattr(GlobalData, "${" + reg_name + "_user_id}", user_id)
    # setattr(GlobalData, f"{reg_name}_user_pwd", password)
    # setattr(GlobalData, f"{reg_name}_user_id", user_id)


def generate_three_user():
    """
    创建三个用户，管理员、投资员、借款人
    :return:
    """
    create_user("admin", type=0)
    create_user("invest")
    create_user("borrow")
    pass


if __name__ == '__main__':
    # print(create_user("admin", type=0))
    # print(create_user("invest"))
    # print(create_user("borrow"))
    # create_user("admin", type=0)
    generate_three_user()

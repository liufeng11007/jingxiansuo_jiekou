# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2020/5/11 20:44 
  @Auth : 可优
  @File : handle_parameterize.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""
# 0、导入re模块
import re


# 1、创建全局数据池类
# 存储全局数据（三个用户账号、未注册的手机号等）
class GlobalData:
    pass


# 2、定义原始字符串
# {"mobile_phone": "${not_existed_tel}", "pwd": "12345678", "type": 1, "reg_name": "KeYou"}
# {"mobile_phone": "18900001111", "pwd": "12345678", "type": 1, "reg_name": "KeYou"}

# one_str = '{"mobile_phone": "${not_existed_tel}", "pwd": "12345678", "type": 1, "reg_name": "KeYou"}'
# one_str = '{"mobile_phone": "${not_existed_tel}", "pwd": "12345678", "uid":" ${user_id}", "type": 1, "reg_name": "KeYou"}'

# 3、定义正则表达式
# a.findall方法将正则匹配上的值放在列表中返回
# b.第一个参数为正则表达式，需要在字符串前加r
# c.第二个参数为待匹配的字符串
# d.如果匹配不上，会返回空列表
# e.$有特殊含义，所以需要使用\来转义
# f. .*?可以匹配任意数据，为非贪婪模式进行匹配
# result = re.findall(r"\${.*?}", one_str)
# for item in result:
#     data = getattr(GlobalData, item)
#     one_str = one_str.replace(item, str(data))


class Parameterize:

    @staticmethod
    def to_parma(src):
        # a.把src字符串中的说哟${}查询出来，返回一个列表
        result = re.findall(r"\${.*?}", src)
        for item in result:
            # b.从全局数据池中读取参数
            data = getattr(GlobalData, item)
            # c.替换指定的数据，然后将原始字符串src覆盖
            # 也可以使用re.sub去替换
            src = src.replace(item, str(data))

        return src


if __name__ == '__main__':
    # one_str = '{"mobile_phone": "${not_existed_tel}", "pwd": "12345678", "uid":" ${user_id}", "type": 1, "reg_name": "KeYou"}'
    two_str = '{"mobile_phone": "${invest_user_tel}", "pwd": "12345678", "reg_name": "KeYou"}'
    setattr(GlobalData, "${not_existed_tel}", "18911112222")
    setattr(GlobalData, "${user_id}", "3333")
    setattr(GlobalData, "${invest_user_tel}", "18911114444")
    Parameterize.to_parma(two_str)
    pass

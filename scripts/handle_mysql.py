import pymysql

import random

from scripts.handle_yaml import do_yaml


class HandleMysql:
    """
    执行sql语句
    """
    def __init__(self):
        self.conn = pymysql.connect(host=do_yaml.get_data('mysql', 'host'),
                                    user=do_yaml.get_data('mysql', 'user'),
                                    password=do_yaml.get_data('mysql', 'password'),
                                    db=do_yaml.get_data('mysql', 'db'),
                                    port=do_yaml.get_data('mysql', 'port'),
                                    charset='utf8',  # 这里只能写为utf8
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def get_one_value(self, sql, args=None):
        self.cursor.execute(sql, args=args)
        self.conn.commit()
        return self.cursor.fetchone()

    def get_values(self, sql, args=None):
        self.cursor.execute(sql, args=args)
        self.conn.commit()
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

    @staticmethod
    def create_mobile():
        """
        随机生成11位手机号
        :return: 返回一个手机号字符串
        """
        start_mobile = ['138', '139', '188']
        start_mobile = random.choice(start_mobile)
        end_num = ''.join(random.sample('0123456789', 8))
        return start_mobile + end_num

    def is_existed_mobile(self, mobile):
        """
        判断指定的手机号在数据库中是否存在
        :param mobile: 11位手机号组成的字符串
        :return: True or False
        """
        # sql = "SELECT mobile_phone FROM member WHERE mobile_phone=%s;"
        sql = do_yaml.get_data('mysql', 'select_user_sql')
        if self.get_one_value(sql, args=[mobile]):  # 手机号已经存在，则返回True，否则返回False
        # if self.get_values(sql, args=[mobile]):  # 手机号已经存在，则返回True，否则返回False
            return True
        else:
            return False

    def create_not_existed_mobile(self):
        """
        随机生成一个在数据库中不存在的手机号
        :return: 返回一个手机号字符串
        """
        while True:
            one_mobile = self.create_mobile()
            if not self.is_existed_mobile(one_mobile):
                break

        return one_mobile

    def get_not_existed_user_id(self):
        # 从yaml配置文件中获取查询最大用户id的sql语句
        sql = do_yaml.get_data('mysql', 'select_max_userid_sql')
        not_existed_id = self.get_one_value(sql).get('id') + 1  # 获取最大的用户id + 1

        return not_existed_id

    def get_not_existed_loan_id(self):
        # 从yaml配置文件中获取查询最大loan id的sql语句
        sql = do_yaml.get_data('mysql', 'select_max_loan_id_sql')
        not_existed_id = self.get_one_value(sql).get('id') + 1  # 获取最大的用户id + 1

        return not_existed_id



if __name__ == '__main__':
    # mobile = '13888888888'
    # sql_1 = "SELECT * FROM member WHERE mobile_phone=%s"
    # sql_2 = "SELECT * FROM member LIMIT 0, 10;"

    do_mysql = HandleMysql()
    print(do_mysql.get_not_existed_user_id())
    # res1 = do_mysql.get_one_value(sql_1, args=(mobile, ))
    # print(res1)
    #
    # res2 = do_mysql.get_values(sql_2)
    # print(res2)
    # do_mysql.create_not_existed_mobile()

    # sql_3 = "SELECT * FROM member LIMIT %s,%s;"
    # print(do_mysql.get_values(sql_3, args=(1, 5)))
    # print(do_mysql.get_values(sql_3, args=[1, 5]))
    # do_mysql.is_existed_mobile("1890000111")

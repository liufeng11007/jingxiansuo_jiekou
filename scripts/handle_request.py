import json

import requests
from scripts.handle_parameterize import GlobalData
from scripts.handle_yaml import do_yaml

# 获取api版本信息
# api_version = do_yaml.get_data("api", "api_version").get("Accept")
# if api_version == "lemonban.v3":   # 如果为v3版本, 才导入HandleSign
#     from scripts.handle_sign import HandleSign


class HandleRequest:

    def __init__(self):
        # 创建会话对象
        self.session = requests.Session()

    def send(self, method, url, **kwargs):
        """
        发送请求的方法
        :param method: 请求方法
        :param url: 请求url
        :param kwargs: headers请求头字典, data、json、files
        :return:
        """
        one_method = method.upper()

        kwargs["json"] = self.handle_param("json", kwargs)
        kwargs["data"] = self.handle_param("data", kwargs)

        # if hasattr(self, 'token') and api_version == "lemonban.v3":  # 如果为v3版本, 则添加sign参数
        #     sign_dict = HandleSign.generate_sign(getattr(self, "token"))  # 生成sign和timestamp组成的字典
        #     # 由于json传参和www-form-encode 不会同时传递
        #     # 只要某一个参数不为None，则合并sign和timestamp参数
        #     if kwargs["json"] is not None:
        #         kwargs["json"].update(sign_dict)
        #     elif kwargs["data"] is not None:
        #         kwargs["data"].update(sign_dict)

        return self.session.request(one_method, url, **kwargs)

    @staticmethod
    def handle_param(param_name, param_dict):

        if param_name in param_dict:
            data = param_dict.get(param_name)
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except Exception:
                    data = eval(data)

            return data
        # else:
        #     return None

    def add_headers(self, one_dict):
        """
        添加公共的请求头
        :param one_dict: 请求头参数，字典类型
        :return:
        """
        self.session.headers.update(one_dict)
        # self.session.headers = one_dict
        # a.判断设置的请求头中是否为Authorization
        if 'Authorization' in one_dict:
            # one_dict = {"Authorization": "Bearer " + token}
            # b.取出token，并设置为动态实例属性
            token = one_dict.get('Authorization').split(' ')[-1]
            setattr(self, "token", token)

    # 获取找线索ID
    def get_ids(self):
        # url = 'https://baize-api.staging.ukuaiqi.com/DataService/api/v1/company/list/multiple'
        url = 'https://baize-api.jingxiansuo.com/DataService/api/v1/company/list/multiple'
        headers = { "Accept" :"application/json"}
        data = {"haveLeads":True,"pageSize":200,"pageIndex":1}
        res = self.send('post', url, json=data)
        if "totalRecords" in res.text:
            total_records = res.json()['data']['totalRecords']
            records = res.json()['data']['records']
            if total_records == 5000:
                ids = []
                id = []
                for i in range(0, 200):
                    if i == 0:
                        id.append(records[i]['id'])
                    else:
                        # print(records[i]['id'])
                        ids.append(records[i]['id'])

                setattr(GlobalData, '${ids}', ids)
                setattr(GlobalData, '${id}', id)

    # 获取跟进中的线索ID
    def get_gjids(self):
        # url = 'https://baize-api.staging.ukuaiqi.com/DataService/publicOcean/getUserFollowClues'
        url = 'https://baize-api.jingxiansuo.com/DataService/publicOcean/getUserFollowClues'
        headers = { "Accept" :"application/json"}
        data = {"pageSize":100,"pageIndex":1,"sortField":"leadsTime","sortType":-1}
        res = self.send('post', url, json=data)
        if "totalRecords" in res.text:
            total_records = res.json()['data']['totalRecords']
            records = res.json()['data']['records']
            if total_records >= 101:
                ids = []
                id = []
                for i in range(0, 100):
                    if i == 0:
                        id.append(records[i]['id'])
                    else:
                        # print(records[i]['id'])
                        ids.append(records[i]['id'])

                setattr(GlobalData, '${gjids}', ids)
                setattr(GlobalData, '${gjid}', id)

    # 获取公海线索ID
    def get_ghxsid(self):
        # url = 'https://baize-api.staging.ukuaiqi.com/DataService/publicOcean/getPublicOceanClues'
        url = 'https://baize-api.jingxiansuo.com/DataService/publicOcean/getPublicOceanClues'
        headers = {"Accept": "application/json"}
        data = {"pageSize":20,"pageIndex":1,"sortField":"discardTime","sortType":-1,"hadExport":""}
        res = self.send('post', url, json=data)
        if "totalRecords" in res.text:
            total_records = res.json()['data']['totalRecords']
            records = res.json()['data']['records']
            if total_records >= 20:
                ids = []
                id = []
                for i in range(0, 20):
                    if i == 0:
                        id.append(records[i]['id'])
                    else:
                        # print(records[i]['id'])
                        ids.append(records[i]['id'])

                setattr(GlobalData, '${ghids}', ids)
                setattr(GlobalData, '${ghid}', id)

    # 获取地图检索ID
    def get_dtjsid(self):
        # url = 'https://baize-api.staging.ukuaiqi.com/DataService/api/v1/company/map/mapCircle'
        url = 'https://baize-api.jingxiansuo.com/DataService/api/v1/company/map/mapCircle'
        headers = {"Accept": "application/json"}
        data = {"haveLeads":True,"pageSize":20,"pageIndex":1,"latPoint":30.714474,"lonPoint":103.932818,"distance":27942.160273502155}
        res = self.send('post', url, json=data)
        if "totalRecords" in res.text:
            total_records = res.json()['data']['totalRecords']
            records = res.json()['data']['records']
            if total_records >= 20:
                ids = []
                id = []
                for i in range(0, 20):
                    if i == 0:
                        id.append(records[i]['id'])
                    else:
                        # print(records[i]['id'])
                        ids.append(records[i]['id'])

                setattr(GlobalData, '${dtids}', ids)
                setattr(GlobalData, '${dtid}', id)

    def close(self):
        """
        释放资源
        :return:
        """
        self.session.close()


if __name__ == '__main__':
    # 1.创建HandleRequest对象
    do_request = HandleRequest()
    # 2.创建登录url
    login_url = "http://api.lemonban.com/futureloan/member/login"

    # 3.构造请求头参数
    headers_dict = {
        "X-Lemonban-Media-Type": "lemonban.v2",
        "User-Agent": "Mozilla/5.0 LookSky"
    }
    # 4.在会话对象中添加请求头
    do_request.add_headers(headers_dict)

    # 5.构造登录参数
    # login_param = {
    #     "mobile_phone": "18511112222",
    #     "pwd": "12345678"
    # }

    login_param = '{"mobile_phone": "18522233479", "pwd": "12345678"}'

    # 6.先登录接口发起请求
    # res = do_request.send("POST", login_url, headers=headers_dict, json=login_param)
    res = do_request.send("POST", login_url, json=login_param)

    # 7.获取登录接口响应体数据，转化为字典类型
    response_data_dict = res.json()
    # 获取token
    token = response_data_dict['data']['token_info']['token']
    # 获取user_id
    user_id = response_data_dict['data']['id']
    pass

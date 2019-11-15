# --*-- coding:utf-8 --*--
import requests
from cacheout import Cache
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
cache = Cache()
appid = 'wx123456789'
app_secret = 'e4123543656768'

def get_token(app_id, app_secret):
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+app_id+'&secret='+app_secret;
    print('get_token  ' + url)
    requests.packages.urllib3.disable_warnings()
    response = requests.get(url, verify=False)
    response = response.json()
    #print(response)
    if response.get('access_token', ''):
        cache.set('access_token', response['access_token'])
        cache.expired('access_token', response['expires_in'])

def notifications(openid, formid):
    if (cache.get('access_token') == None):
        get_token(appid, app_secret)

    access_token = cache.get('access_token')

    template_id = 'RhvXx9BYeLtpEVnff0mrbC0PutYDDDOLLH3VqIjtPT4'
    push_data = {
        "keyword1": {
            "value": 'test',
            "color": "#4a4a4a"
        },
        "keyword2": {
            "value": '17623205062',
            "color": "#9b9b9b"
        },
        "keyword3": {
            "value": '查询到数据，请核实真实性。',
            "color": "red"
        },
        "keyword4": {
            "value": '2017-01-21 13:10:10',
            "color": "blue"
        },
        "keyword5": {
            "value": '3505xxxxxxxxxxxxxx'
        },
        "keyword6": {
            "value": 'abc'
        },
        "keyword7": {
            "value": '20191115'
        },
        "keyword8": {
            "value": '3'
        },
    }

    if access_token:
        # 如果存在accesstoken
        payload = {
            'touser': openid, #这里为用户的openid
            'template_id': template_id, #模板id
            'page': 'pages/index/index',
            'form_id': formid, #表单id或者prepay_id
            'data': push_data #模板填充的数据
        }

        url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token='+access_token
        requests.packages.urllib3.disable_warnings()
        response = requests.post(url, json=payload, verify=False)

        #直接返回res结果
        return response.json()
    else:
        return {
            'err': 'access_token missing'
        }


if __name__ == '__main__':
    print('notification')
    #get_token(appid, app_secret)
    #res = notifications('f6f95d5f99823434540ea', 'oLxWq5TGgCHJdVdOo1Qwc4_jf1AU')
    #print(res)
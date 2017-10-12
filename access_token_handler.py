# Handle access_token for wechat, with the help of access_token.json file
#-*-coding:utf-8 -*-

import json
import requests
import time

def get_access_token():
    url = ('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_' +
          'credential&appid=wxddae0de1b0e43c9e&secret=3694ea0bc550f58' +
          '15547d4e182ab42b3')
    print url
    response = requests.get(url)
    data = response.json()
    data['create_time'] = time.time()
    with open('access_token.json', 'w') as outfile:
        json.dump(data, outfile)
    return data['access_token']

def check_expire():
    with open('access_token.json') as data:
        d = json.load(data)
    if 'create_time' in d:
        if d['create_time'] + 6000 > time.time():
            return False # no key create_time exists, need to update access_token
    return True

# Handle access_token for wechat, with the help of access_token.json file
#-*-coding:utf-8 -*-

import json
import requests
import time

def new_access_token():
    # appid = 'wxddae0de1b0e43c9e' # 彭若波robby
    # appsecret = '3694ea0bc550f5815547d4e182ab42b3' # 彭若波robby
    appid = 'wxb8b26cc7a6236b84' # KiwiLens
    appsecret = 'c39de4105ea7929132829e2cf0606ba8' # KiwiLens
    url = ('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_' +
          'credential&appid=%s&secret=%s')
    url = url % (appid, appsecret)
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

def retrieve_token():
    with open('access_token.json') as data:
        d = json.load(data)
    return d['access_token']

def get_token():
    try:
        check_expire()
    except (ValueError, IOError):
        return new_access_token()
    if check_expire():
        return new_access_token()
    else:
        return retrieve_token()

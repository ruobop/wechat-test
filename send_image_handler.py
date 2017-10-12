#-*-coding:utf-8 -*-
# Handle sending images to wechat
# http请求方式：POST/FORM，使用https
# https://api.weixin.qq.com/cgi-bin/media/upload?access_token=ACCESS_TOKEN&type=TYPE
# 正确情况下的返回JSON数据包结果如下：
# {"type":"TYPE","media_id":"MEDIA_ID","created_at":123456789}

import access_token_handler
import time
import xml.etree.ElementTree as ET
import sys

def upload_temp_media(filepath):
    access_token = access_token_handler.get_token()
    type = 'image'
    url = ('https://api.weixin.qq.com/cgi-bin/media/upload?access_token=' +
           '%s&type=%s')
    url = url % (access_token, type)
    files = {'media': open(filepath, 'rb')}
    response = requests.post(url, files=files)
    data = response.json()
    if 'MEDIA_ID' in data:
        return data['MEDIA_ID']
    else:
        return 'error'

def make_imgmsg(filepath, fromuser, touser):
    for i in range(0, 5): # try upload 5 times
        media_id = upload_temp_media(filepath)
        if media_id != 'error':
            reply = """
            <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                <MediaId><![CDATA[%s]]></MediaId>
                </Image>
            </xml>
        	"""
            resp_str = reply % (touser, fromuser, int(time.time()), media_id)
            return resp_str
    sys.exit('error when getting media_id!')

# -*- coding:utf-8 -*-
import json
import access_token_handler
import requests
import time
import xml.etree.ElementTree as ET
import sys
from celery import Celery
def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

def send_text_msg(text, fromuser, touser):
    print touser
    raw_data = """
    {
        "touser":"%s",
        "msgtype":"text",
        "text":
        {
            "content":"%s"
        }
    }
    """
    raw_data = raw_data % (touser, text)
    json_data = json.dumps(json.loads(raw_data))
    print json_data
    access_token = access_token_handler.get_token()
    url = ('https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' +
           '%s')
    url = url % (access_token)
    headers = {'content-type': 'application/json'}
    time.sleep(5)
    response = requests.post(url, json_data, headers=headers)
    print response.content

def saveimg(oridata, filepath):
    xmldata = ET.fromstring(oridata)
    picurl = xmldata.find("PicUrl").text
    urllib.urlretrieve(picurl, filepath) # save url to jpg file

def sendimg(image_path, url_port):
    f = open(image_path,'rb')
    files = {'file': f}
    headers = {'content-type': 'image/jpeg'}
    response = requests.post(url_port, files = files)
    f.close()
    return response

def upload_temp_media(filepath):
    access_token = access_token_handler.get_token()
    type = 'image'
    url = ('https://api.weixin.qq.com/cgi-bin/media/upload?access_token=' +
           '%s&type=%s')
    url = url % (access_token, type)
    files = {'media': open(filepath, 'rb')}
    response = requests.post(url, files=files)
    data = response.json()
    if 'media_id' in data:
        return data['media_id']
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

from wechat import celery
import time
import json
import requests
import access_token_handler
@celery.task()
def save_send_img(oridata, savepath, url_port, sendpath, fromuser, touser):
    saveimg(oridata, savepath)
    out_image_raw = sendimg(savepath, url_port)
    with open(sendpath, 'wb') as f:
        for chunk in out_image_raw.iter_content():
            f.write(chunk)
    make_imgmsg(sendpath, fromuser, touser)

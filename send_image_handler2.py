from flask import Flask
from celery import Celery
import celery
import json
import access_token_handler
import requests
import time
import send_msg_celery

@celery.task()
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

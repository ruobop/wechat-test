# -*- coding:utf-8 -*-
from celery import Celery
import time
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

from wechat import celery
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

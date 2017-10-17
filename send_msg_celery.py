#-*-coding:utf-8 -*-
from flask import Flask
app = Flask(__name__)
from celery import Celery

#from celery import platforms  #如果你不是linux的root用户，这两行没必要
#platforms.C_FORCE_ROOT=True   #允许root权限运行celery

def make_celery(app):
    celery = Celery(app.import_name,  #此处官网使用app.import_name，因为这里将所有代码写在同一个文件flask_celery.py,所以直接写名字。
                     broker=app.config['CELERY_BROKER_URL'],
                     backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/1'
)
celery = make_celery(app)

@celery.task()
def long_time_def():
    for _ in range(100):
        for j in range(100):
            i = 1
    return 'hello'

@app.route("/")
def hello():
    print ("耗时的任务")
    result=long_time_def.apply_async()   #变化在这里
    return '耗时的任务已经交给了celery'

if __name__ == "__main__":
    app.run(debug=True)

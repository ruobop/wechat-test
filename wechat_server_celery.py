#-*-coding:utf-8 -*-
from flask import Flask, request
# from flask import make_response
# import hashlib
# import MsgParser
# from send_image_handler2 import send_text_msg
# import send_msg_celery
# import json
# import access_token_handler
# import requests
# import time
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
# response at 127.0.0.1/weixin/
@app.route('/weixin', methods=['GET', 'POST'])
def weixin():
    if request.method == 'GET':
        if len(request.args) > 3:
            temparr = []
            token = "thisisatest"
            signature = request.args["signature"]
            timestamp = request.args["timestamp"]
            nonce = request.args["nonce"]
            echostr = request.args["echostr"]
            temparr.append(token)
            temparr.append(timestamp)
            temparr.append(nonce)
            temparr.sort()
            newstr = "".join(temparr)
            sha1str = hashlib.sha1(newstr)
            temp = sha1str.hexdigest()
            if signature == temp:
                return echostr
            else:
                return "Authentification failed!"
        else:
            return "Your request method is: " + request.method
#     elif request.method == 'POST':  # POST
#         # print "POST"
#         oridata = request.data # store incoming data
#         data_xmldict = MsgParser.simple_parser(oridata)
#         if data_xmldict['type'] == 'image':
#             # reply = MsgParser.make_textmsg('收到了图片！', data_xmldict['to'],
#             #                               data_xmldict['from'])
#             # send back 'success', push work into back queue
#             reply = MsgParser.make_textmsg('正在处理中，请稍候！',
#                                       data_xmldict['to'], data_xmldict['from'],)
#             send_text_msg.delay('Hello World!', data_xmldict['to'],
#                           data_xmldict['from'])
#             # work on back queue
#         else:
#             reply = MsgParser.make_textmsg('没有收到图片，请发给我图片！',
#                                       data_xmldict['to'], data_xmldict['from'],)
#         response = make_response(reply)
#         response.content_type = 'application/xml'
#         return response

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80)

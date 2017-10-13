# python response_image.py responses request from wechat server
#-*-coding:utf-8 -*-

from flask import Flask, request
from flask import make_response
import hashlib
import MsgParser
import send_image_handler
app = Flask(__name__)

# response at 127.0.0.1/
@app.route('/')
def hello_world():
    return 'Hello World!'

# response at 127.0.0.1/ssd
@app.route('/ssd', methods=['GET', 'POST'])
def ssd():
    if request.method == 'POST':
        # fetch http POST data
        in_image = request.data
        # process image, send image to ssd detection
        out_image = ssd(in_image)
        # process out image, make out image to response
        response = make_response(out_image)
        # return out image within response
        return response

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
    elif request.method == 'POST':  # POST
        # print "POST"
        oridata = request.data # store incoming data
        data_xmldict = MsgParser.simple_parser(oridata)
        if data_xmldict['type'] == 'image':
            # reply = MsgParser.make_textmsg('收到了图片！', data_xmldict['to'],
            #                               data_xmldict['from'])
            savepath = '/home/ubuntu/savedImg/1.jpg'
            MsgParser.saveimg(oridata, savepath)
            sendpath = savepath
            # 发送图片给用户
            reply = send_image_handler.make_imgmsg(sendpath, data_xmldict['to'],
                                                   data_xmldict['from'])
        else:
            reply = MsgParser.make_textmsg('没有收到图片，请发给我图片！',
                                      data_xmldict['to'], data_xmldict['from'],)
        response = make_response(reply)
        response.content_type = 'application/xml'
        return response

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 9527)

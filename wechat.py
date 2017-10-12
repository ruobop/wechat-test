# python wechat.py responses request from wechat platform
#-*-coding:utf-8 -*-
from flask import Flask, request
from flask import make_response
import hashlib
import MsgParser
app = Flask(__name__)

# response at 127.0.0.1/
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
    elif request.method == 'POST':  # POST
        # print "POST"
        xmldict = MsgParser.recv_msg(request.data)
        # print '***' + xmldict['MsgType'] + '***'
        if xmldict['MsgType'] != 'img':
            reply = MsgParser.submit_msg(xmldict)
            response = make_response(reply)
            response.content_type = 'application/xml'
            return response
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80)

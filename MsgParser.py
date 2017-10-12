# MsgParser module
#-*-coding:utf-8 -*-
import time
import xml.etree.ElementTree as ET
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def recv_msg(oriData):
    """
    获取从微信服务器post而来的消息
    :param oriData: post的data
    :return:返回一个包含发送者、接收者、消息内容的字典
    """
    xmldata = ET.fromstring(oriData)
    # 获取发送方的ID
    fromusername = xmldata.find("FromUserName").text
    # 接收方的ID
    tousername = xmldata.find("ToUserName").text
    # 消息的内容
    content = xmldata.find("Content").text
    # 消息的类型
    msgtype = xmldata.find("MsgType").text
    xmldict = {"FromUserName": fromusername, "ToUserName": tousername,
               "MsgType": msgtype, "Content": content}
    return xmldict
def submit_msg(content_dict={"": ""}, type="text"):
    """
    编制回复信息
    :param content_dict:
    :param type:
    :return:
    """
    toname = content_dict["FromUserName"]
    fromname = content_dict["ToUserName"]
    content = content_dict["Content"]
    content = "没有收到图片，请发给我图片！"
    reply = """
    <xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        <FuncFlag>0</FuncFlag>
    </xml>
	"""
    resp_str = reply % (toname, fromname, int(time.time()), content)
    return resp_str
def msg_type(oridata):
    """
    编制回复信息
    :param content_dict:
    :param type:
    :return:
    """
    xmldata = ET.fromstring(oridata)
    datatype = xmldata.find("MsgType").text
    return datatype

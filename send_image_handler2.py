import json
import access_token_handler
import requests

def send_text_msg(text, fromuser, touser):
    raw_data = """
    {
        "touser":%s,
        "msgtype":"text",
        "text":
        {
            "content":%s
        }
    }
    """
    raw_data = raw_data % (touser, text)
    json_data = json.dumps(raw_data)
    access_token = access_token_handler.get_token()
    url = ('https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' +
           '%s')
    url = url % (access_token)
    payload = {'some': 'data'}
    headers = {'content-type': 'application/json'}

    response = requests.post(url, json_data, headers=headers)

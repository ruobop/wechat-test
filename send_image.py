#-*-coding:utf-8 -*-
# Runs on wechat server, to send local image to SSD server

import requests

def send_image_to_ssd(image_path, url_port):
    f = open(image_path,'rb')
    files = {'file': f}
    headers = {'content-type': 'image/jpeg'}
    response = requests.post(url_port, files = files)
    f.close()
    return response

filepath = '/home/ruobo/Desktop/VOC2019/JPEGImages/IMG_3703.jpg'
url = 'http://127.0.0.1:9527'
response = send_image_to_ssd(filepath, url)
image_name = 'out_image.png'
with open(image_name, 'wb') as f:
    for chunk in response.iter_content():
        f.write(chunk)

# r = send_image_to_ssd(filepath, url)

# if r.text == 'success':

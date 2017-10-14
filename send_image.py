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

# filepath = '/home/ruobo/Desktop/paomian/IMG_20170928_101715.jpg'
# url = 'http://54.223.170.185:9527'
# response = send_image_to_ssd(filepath, url)
# image_name = 'out_image.png'
# with open(image_name, 'wb') as f:
#     for chunk in response.iter_content():
#         f.write(chunk)

# r = send_image_to_ssd(filepath, url)

# if r.text == 'success':

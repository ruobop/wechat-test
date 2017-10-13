#-*-coding:utf-8 -*-
import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import plot_label

UPLOAD_FOLDER = '/home/ruobo/Desktop/wechat/wechat-test/wechat-test/'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
# app._static_folder = '/home/ruobo/Desktop/wechat/wechat-test/wechat-test/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No selected file'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename('in_image.jpg')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print '***********\n' + 'Processing image!\n' + '***********'
            plotlabel.ssdetect('in_image.jpg', 'ssd_in_image')
            return send_from_directory('/home/ruobo/Desktop/wechat/wechat-test/wechat-test/',
                                       'ssd_in_image.png')
            # return app.send_static_file('in_image.jpg')
            # return redirect(url_for('uploaded_file',
            #                        filename=filename))
            # return 'file upload seccessfully!'
    return 'No selected file'
#
# @app.route('/<path:filename>')
# def send_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
#
# @app.route('/result/<path:path>')
# def send_js(path):
#     return send_from_directory('js', path)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 9527)

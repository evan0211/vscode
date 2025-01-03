# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 17:52:31 2024

@author: udoo_w2
"""
from flask import Flask, request, redirect, flash#, url_for
import os

# 初始化 Flask
app = Flask(__name__)

# 設定存放上傳照片的資料夾
UPLOAD_FOLDER = 'uploaded_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 限制上傳檔案大小
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制檔案大小為16MB

# 允許的檔案格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 檢查檔案是否允許的格式
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 上傳照片的路由
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    files = request.files.getlist('files[]')

    for file in files:
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return 'Files successfully uploaded'

# 啟動 Flask 伺服器
if __name__ == '__main__':
    app.run(host='120.108.111.124', port=5000)

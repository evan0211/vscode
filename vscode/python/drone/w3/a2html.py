# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:17:52 2024

@author: udoo_w2
"""
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # 讀取CSV檔案
    df = pd.read_csv(r'python\drone\pose_landmarks.csv')
    
    # 只提取 x, y, z 三個欄位
    df = df[['x', 'y', 'z']]
    
    # 將資料轉換為字典
    data = df.to_dict(orient='records')
    
    # 渲染網頁並傳遞資料
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)



# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 17:56:42 2024

@author: ren
"""

import requests

# 上傳的目標URL
url = 'http://120.108.111.124:5000/upload'

# 要上傳的圖片檔案路徑
files = [
    ('files[]', open('img/1.jpg', 'rb')),
    ('files[]', open('img/2.jpg', 'rb'))
]
 
# 發送 POST 請求上傳照片
response = requests.post(url, files=files)

print(response.text)

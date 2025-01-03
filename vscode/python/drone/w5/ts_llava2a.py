# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 15:03:04 2024

@author: udoo_w2
"""
from ollama import Client
client = Client(host='http://localhost:11434')

file = '1.jpg'

res = client.chat(
    model="llava-phi3:latest",
    messages=[
        {
            'role':'user',
            'content':"describe this picture.",
            'images':['./img/'+file]
            }
        ]
    )
ans=res['message']['content']
print(ans)
if "Yes" in ans:
    print("received")

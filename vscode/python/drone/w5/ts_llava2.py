# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 15:03:04 2024

@author: udoo_w2
"""
import ollama

file = '1.jpg'
res = ollama.chat(
    model="llava-phi3:latest",
    messages=[
        {
            'role':'user',
            'content':"Is the computer mouse placed next to the hand in this image?",
            'images':['./img/'+file]
            }
        ]
    )
print(res['message']['content'])

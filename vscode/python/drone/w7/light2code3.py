# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 13:48:41 2024

@author: udoo_w2
"""
import cv2  
import numpy as np  
import pandas as pd  
import os
#import subprocess
from ultralytics import YOLO

# import supervision as sv
# from roboflow import Roboflow
import warnings
import torch
# 忽略 FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)
HOME = os.getcwd()
#print(HOME)
model_path="train2"
model = YOLO(f'{HOME}/{model_path}/weights/best.pt')


# 摩爾斯碼對應的字母表  
MORSE_CODE_DICT = {  
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',  
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',  
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',  
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',  
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',  
    '--..': 'Z',  
    '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',  
    '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9'  
}  
  
# 全局變量，用於存儲矩形範圍座標  
start_point = None  
end_point = None  
  
def select_rectangle(event, x, y, flags, param):  
    global start_point, end_point  
  
    if event == cv2.EVENT_LBUTTONDOWN:  # 滑鼠按下，開始選取矩形範圍  
        start_point = (x, y)  
    elif event == cv2.EVENT_LBUTTONUP:  # 滑鼠放開，結束選取  
        end_point = (x, y)  
  
def get_brightness(frame, start_point, end_point):  
    """計算給定幀的指定範圍的平均亮度"""  
    x1, y1 = min(start_point[0], end_point[0]), min(start_point[1], end_point[1])  
    x2, y2 = max(start_point[0], end_point[0]), max(start_point[1], end_point[1])  
  
    roi = frame[y1:y2, x1:x2]  
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)  
    return np.mean(gray_roi)  
  
def decode_morse_from_brightness(csv_path):  
    # 讀取 CSV 文件  
    df = pd.read_csv(csv_path)  
  
    current_morse_char = ""  
    count = 0  
    space_count = 0  # 用於計數間隔  
    decoded_message = ""  
  
    for index, row in df.iterrows():  
        brightness = row['Brightness']  
  
        if brightness > 58:  
            count += 1  # 計數長亮  
            if space_count > 0:  # 如果之前有間隔，印出間隔數  
                print(f"Space Count: {space_count}")  
                space_count = 0  # 重置間隔計數  
        else:  
            if count > 16:  # 判斷長亮  
                current_morse_char += '-'  
            elif count > 3:  # 判斷短亮  
                current_morse_char += '.'  
            count = 0  # 重置計數  
  
            space_count += 1  # 計數間隔  
  
        # 檢查是否到達字母的結束（間隔時間較長）  
        if index > 0 and brightness < 10:  # 假設亮度小於10表示間隔  
            if current_morse_char:  
                if current_morse_char in MORSE_CODE_DICT:  
                    decoded_message += MORSE_CODE_DICT[current_morse_char]  
                    print(f"Decoded Character: {current_morse_char} -> {MORSE_CODE_DICT[current_morse_char]}")  
                current_morse_char = ""  
  
    # 印出最後的間隔數  
    if space_count > 0:  
        print(f"Space Count: {space_count}")  
  
    # return decoded_message  
    return current_morse_char
  
def decode_morse_from_video(video_path):  
    cap = cv2.VideoCapture(video_path)  
    cap.set(cv2.CAP_PROP_POS_FRAMES, 600)  
    ret, frame = cap.read()  
  
    if not ret:  
        print("無法讀取第600幀")  
        cap.release()  
        return  
  
    # cv2.namedWindow('Frame')  
    # cv2.setMouseCallback('Frame', select_rectangle)  
  
    # print("請使用滑鼠選取範圍，然後按 'q' 確認")  
    # while True:  
    #     cv2.imshow('Frame', frame)  
    #     key = cv2.waitKey(1) & 0xFF  
    #     if key == ord('q') and start_point and end_point:  
    #         break  
  
    cap.set(cv2.CAP_PROP_POS_FRAMES, 600)  
    brightness_values = []  
    while cap.isOpened():  
        ret, frame = cap.read()  
        if not ret:  
            break  
        # 每一幀儲存為 .jpg 檔案
        frame_filename = f'{HOME}/data/light.jpg'
        cv2.imwrite(frame_filename, frame)
        
        results = model(source=frame_filename, conf=0.25)
        # 获取置信度分数  
        confidences = results[0].boxes.conf
        # 检查置信度分数是否为空  
        if confidences.numel() == 0:  
            start_point = (330,92)
            end_point = (402,219)
            brightness = get_brightness(frame, start_point, end_point)  
            brightness_values.append(brightness)
                                
        else:
            # 找到最大置信度的索引  
            max_conf_index = torch.argmax(confidences)  
          
            # 使用该索引来获取相应的 class_id  
            class_id = results[0].boxes.cls[max_conf_index].item()
            #print("cls: ",results[0].boxes.cls)
            #class_id = results[0].boxes.cls.item()
            #print("Object type:", class_id) 
            if class_id == 0.0:
                cords = results[0].boxes.xyxy[0].tolist()
                x1=cords[0]
                y1=cords[1]
                x2=cords[2]
                y2=cords[3]
                #print("image.shape=",image.shape)
                #print(f'x1={x1},y1={y1},x2={x2},y2={y2}')
                # left = x1
                # top = y1
                # right = x2
                # bottom = y2
                start_point = (int(x1),int(y1))
                end_point = (int(x2),int(y2))
                
                #width = right - left
                #height = bottom - top
                #bbox = (int(left), int(top), int(width), int(height))
            brightness = get_brightness(frame, start_point, end_point)  
            brightness_values.append(brightness)  
  
    cap.release()  
  
    # 將亮度值存儲到 CSV 文件  
    brightness_df = pd.DataFrame(brightness_values, columns=['Brightness'])  
    brightness_df.to_csv('brightness.csv', index=False)  
  
# 使用影片來解碼摩爾斯密碼  
video_path = 'flashlight_morse.mp4'  
decode_morse_from_video(video_path)  
  
# 使用 CSV 文件來解碼摩爾斯密碼  
csv_path = 'brightness.csv'  
decoded_message = decode_morse_from_brightness(csv_path)  
print(f"Decoded Morse Message: {decoded_message}")  

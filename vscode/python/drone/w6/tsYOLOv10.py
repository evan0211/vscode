# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 17:14:23 2024

@author: udoo_w2
"""
# conda activate py311
# TORCH_USE_CUDA_DSA=1 python trYOLOv10b.py

import os
#import subprocess
from ultralytics import YOLO
import cv2
#import supervision as sv
# from roboflow import Roboflow
import warnings

# 忽略 FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)

# ROBOFLOW_API_KEY = 'ywImedzWFsd5ttjhyF3x'

# rf = Roboflow(api_key=ROBOFLOW_API_KEY)
# project = rf.workspace("selencakmak").project("tumor-dj2a1")
# version = project.version(1)
# dataset = version.download("yolov8")

HOME = os.getcwd()
#print(HOME)
model_path="train3"
model = YOLO(f'{HOME}/{model_path}/weights/best.pt')
results = model(source=f'{HOME}/data/drone.jpg', conf=0.35)
image = cv2.imread(f'{HOME}/data/drone.jpg') 
print(results[0].boxes.xyxy)#,results[0].boxes.conf,results[0].boxes.cls)
class_id = results[0].boxes.cls.item()
print("Object type:", class_id) 
if class_id == 0.0:
    cords = results[0].boxes.xyxy[0].tolist()
    x1=cords[0]
    y1=cords[1]
    x2=cords[2]
    y2=cords[3]
    print("image.shape=",image.shape)
    print(f'x1={x1},y1={y1},x2={x2},y2={y2}')
    left = x1
    top = y1
    right = x2
    bottom = y2
    
    width = right - left
    height = bottom - top
    bbox = (int(left), int(top), int(width), int(height))
    
    drone_img=image[int(bbox[1]):int(bbox[1] + bbox[3]), int(bbox[0]):int(bbox[0] + bbox[2]),:] # for jpg
    cv2.imwrite(f'{HOME}/data/drone2.jpg', drone_img) 
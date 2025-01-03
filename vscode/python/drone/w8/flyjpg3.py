# -*- coding: utf-8 -*-  
import sys  
import traceback  
from djitellopy import Tello, TelloException  
import cv2  
#import numpy as np  
from time import sleep  
import threading  
import os  
import shutil  
  
def setup_img_folder():  
    img_folder = "img"  
    if os.path.exists(img_folder):  
        shutil.rmtree(img_folder)  
    os.makedirs(img_folder)  
  
def process_video(drone):  
    retry = 30  
    cap = None  
    while cap is None and 0 < retry:  
        retry -= 1  
        try:  
            cap = cv2.VideoCapture(drone.get_udp_video_address())  
        except Exception as e:  
            print(e)  
      
    frame_skip = 300  
    img_use = 0  
    try:  
        while True:  
            ret, frame = cap.read()  
            if not ret:  
                print("Frame is None, exiting loop.")  
                break  
  
            if frame_skip > 0:  
                frame_skip -= 1  
                continue  
  
            img_use += 1  
            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  
  
            if img_use > 2500:  
                img_use = 1  
  
            cv2.imwrite("img/" + str(img_use) + ".jpg", image)  
    except Exception as e:  
        print(f"An unexpected error occurred: {e}")  
    finally:  
        print("Exiting video processing thread.")  
        cap.release()  
  
def handle_keyboard_input(drone):  
    while True:  
        user_input = input("Enter your command: ")  
        # 处理用户输入的逻辑，例如更新 frame_skip 或其他变量  
        print(f"User entered: {user_input}")  
        if user_input == "q":  
            drone.end()  
            break  
        if user_input == "1":  
            try:  
                drone.takeoff()  
                print("takeoff")  
                sleep(5)  
            except TelloException as e:  
                print(f"Error during takeoff: {e}")  
        if user_input == "2":  
            try:  
                drone.rotate_clockwise(25)  # 1-360
                print("clockwise")  
                sleep(5) 
            except TelloException as e:  
                print(f"Error during rotation: {e}")  
        if user_input == "3":  
            try:  
                drone.rotate_counter_clockwise(25)  # 1-360
                print("counter_clockwise")  
                sleep(5) 
            except TelloException as e:  
                print(f"Error during rotation: {e}")  
        if user_input == "4":  
            try:  
                drone.land()  
                print("land")  
                sleep(5)  
            except TelloException as e:  
                print(f"Error during landing: {e}")    
        if user_input == "5":  
            try:  
                execute_path(drone)  
                print("Executing path")  
            except TelloException as e:  
                print(f"Error during path execution: {e}")  
        if user_input == "6":  
            try:  
                execute_path2(drone)  
                print("Executing path")  
            except TelloException as e:  
                print(f"Error during path execution: {e}")  

def execute_path(drone):  
    # 定义相对于当前点的增量 (dx, dy, dz)，单位为厘米  
    increments = [  
        (30, -30, 30)#,   # 向前右上方移动30厘米  
        # (-30, -30, -30), # 向后右下方移动30厘米  
        # (-30, 30, 30),   # 向后左上方移动30厘米  
        # (30, 30, -30)    # 向前左下方移动30厘米  
    ]  
  
    speed = 20  # 设置移动速度，单位为厘米每秒  
  
    for increment in increments:  
        dx, dy, dz = increment  
        try:  
            drone.go_xyz_speed(dx, dy, dz, speed)  
            sleep(5)  # 等待无人机到达目标点  
        except TelloException as e:  
            print(f"Error during moving to increment {increment}: {e}") 
                
def execute_path2(drone):  
    # 定义相对于当前点的增量 (x1, y1, z1) 和 (x2, y2, z2)，单位为厘米  
    curves = [  
        ((30, 30, 30), (60, 60, 60))#,   # 第一个曲线段  
        # ((-30, 30, -30), (-60, 60, -60)), # 第二个曲线段  
        # ((-30, -30, 30), (-60, -60, 60)), # 第三个曲线段  
        # ((30, -30, -30), (60, -60, -60))  # 第四个曲线段  
    ]  
  
    speed = 20  # 设置移动速度，单位为厘米每秒  
  
    for curve in curves:  
        (x1, y1, z1), (x2, y2, z2) = curve  
        try:  
            drone.curve_xyz_speed(x1, y1, z1, x2, y2, z2, speed)  
            sleep(5)  # 等待无人机到达目标点  
        except TelloException as e:  
            print(f"Error during moving along curve {curve}: {e}")  
  
# 设置 img 文件夹  
setup_img_folder()  
  
drone = Tello()  
try:  
    drone.connect()  
    drone.streamon()  
except Exception as ex:  
    exc_type, exc_value, exc_traceback = sys.exc_info()  
    traceback.print_exception(exc_type, exc_value, exc_traceback)  
    print(ex)  
  
# 创建并启动视频处理线程  
video_thread = threading.Thread(target=process_video, args=(drone,))  
video_thread.start()  
  
# 创建并启动键盘输入处理线程  
keyboard_thread = threading.Thread(target=handle_keyboard_input, args=(drone,))  
keyboard_thread.start()  
  
# 等待两个线程结束  
video_thread.join()  
keyboard_thread.join()  

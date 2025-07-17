# -*- coding: utf-8 -*-
import sys
import traceback
import tellopy
import av
import cv2
import numpy
from time import sleep
import threading
import numpy as np

def process_video(drone):
    retry = 30
    container = None
    while container is None and 0 < retry:
        retry -= 1
        try:            
            container = av.open(drone.get_video_stream())
        except av.AVError as ave:
            print(ave)
            
    frame_skip = 300
    img_use = 0
    
    try:
        while True:
            for frame in container.decode(video=0):
                if frame is None:
                    print("Frame is None, exiting loop.")
                    break
                
                if frame_skip > 0:
                    frame_skip -= 1
                    continue
                
                img_use += 1
                image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                
                if img_use > 2500:
                    img_use = 1
                
                cv2.imwrite("img/" + str(img_use) + ".jpg", image)
            else:
                # If the inner loop is exhausted without hitting the break, continue
                continue
            # If the inner loop breaks, break the outer loop as well
            break
    except av.AVError as e:
        print(f"Error decoding video: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Exiting video processing thread.")

def handle_keyboard_input(drone):
    while True:
        user_input = input("Enter your command: ")
        # 处理用户输入的逻辑，例如更新 frame_skip 或其他变量
        print(f"User entered: {user_input}")
        if user_input == "q":
            drone.quit()
            break
        if user_input == "1":
            drone.takeoff() 
            print("takeoff")
            sleep(5)
        if user_input == "2":
            drone.clockwise(25)
            print("clockwise")
            sleep(4) # sleep(1): 10 degree?       
            drone.counter_clockwise(0)
            sleep(2)
        if user_input == "3":
            drone.counter_clockwise(25)
            print("counter_clockwise")
            sleep(4)       
            drone.clockwise(0)                    
            sleep(2)        
        if user_input == "4":
            drone.land()
            print("land")
            sleep(2)            
        
drone = tellopy.Tello()
try:
    drone.connect()    
    drone.wait_for_connection(60.0)          
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
                

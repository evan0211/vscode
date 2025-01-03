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

import time
from pywifi import PyWiFi, const, Profile
import sqlite3
  

def connect_to_wifi(ssid, password=None):
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]  # 使用第一個WiFi介面

    iface.scan()  # 開始掃描
    time.sleep(2)  # 等待掃描完成

    scan_results = iface.scan_results()
    profile = None

    for result in scan_results:
        if result.ssid == ssid:
            profile = Profile()
            profile.ssid = ssid
            profile.auth = const.AUTH_ALG_OPEN  # 開放認證
            
            if password:  # 如果有提供密碼
                profile.akm.append(const.AKM_TYPE_WPA2PSK)  # WPA2 PSK
                profile.cipher = const.CIPHER_TYPE_CCMP  # 加密類型
                profile.key = password  # 設置密碼
            else:  # 如果無密碼
                profile.akm.append(const.AKM_TYPE_NONE)  # 無加密
                
            break

    if profile is None:
        print(f"未找到SSID為 {ssid} 的網路")
        return

    iface.remove_all_network_profiles()  # 移除所有已保存的網路
    iface.add_network_profile(profile)  # 添加新的網路配置
    iface.connect(profile)  # 連接到指定網路

    time.sleep(10)  # 等待連接

    if iface.status() == const.IFACE_CONNECTED:
        print(f"成功連接到 {ssid}")        
        
        def read_last_entries(limit=10):  
            conn = sqlite3.connect('./hand_detection.db')  # 連接到本地SQLite數據庫
            cursor = conn.cursor()  
            cursor.execute(f'SELECT * FROM hand_detection ORDER BY id DESC LIMIT {limit}')  # 讀取最新的手勢檢測數據
            entries = cursor.fetchall()  
            conn.close()  
            return entries
        
        def process_video(drone):  
            frame_skip = 300  # 設置跳過的幀數以減少負荷
            while True:  # 外層循環允許重新獲取幀  
                retry = 30  # 設置重試次數
                container = None  
                  
                while container is None and retry > 0:  # 如果容器為空且重試次數還有剩餘
                    retry -= 1  
                    try:  
                        container = av.open(drone.get_video_stream())  # 嘗試打開無人機的視訊流
                    except av.AVError as ave:  
                        print(ave)  # 捕獲異常並打印
          
                  
                img_use = 0  # 計數用來追蹤已處理幀數
          
                try:  
                    while True:  
                        for frame in container.decode(video=0):  # 解碼視訊流中的幀
                            if frame is None:  # 如果幀為空，退出循環
                                print("Frame is None, exiting loop.")  
                                break  
          
                            # 根據需求跳過幀
                            if frame_skip > 0:  
                                frame_skip -= 1  
                                continue  
          
                            img_use += 1  # 增加已使用幀的計數
                            image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)  # 將幀轉換為OpenCV的BGR格式
                            cv2.imwrite("img/" + str(img_use) + ".jpg", image)  # 將圖像保存到本地
                            
                                
                            if img_use >= 5:  # 如果已保存的圖像數量達到5，退出內層循環
                                break
          
                        # 檢查是否需要清空緩衝區
                        if img_use >= 5:  # 例如：滿足條件時重置
                            img_use = 0
                            print("Clearing buffer, re-fetching frames.")  # 清空緩衝區並重新獲取幀
                            
                            # 示例：讀取最後 10 條記錄  
                            last_records = read_last_entries()  # 讀取手勢檢測的最後10筆記錄
                            total_left_position = 0  
                            total_right_position = 0  
                              
                            for record in last_records:  # 累積左手和右手的位置
                                id, timestamp, left_hand_position, right_hand_position = record  
                                total_left_position += left_hand_position  
                                total_right_position += right_hand_position  
                              
                            # 檢查加總是否超過 5  
                            if total_left_position > 5 or total_right_position > 5:  # 如果加總的值超過5
                                
                                drone.land()  # 無人機降落
                                print("land")
                                sleep(5)  # 等待降落
                                
                                drone.quit()  # 退出無人機的連接
                                
                                print("符合條件的記錄:")  
                                for record in last_records:  # 打印符合條件的記錄
                                    print(f"ID={record[0]}, 時間戳={record[1]}, 左手位置={record[2]}, 右手位置={record[3]}")
                                
                            else:  
                                print("沒有符合條件的記錄。")  # 如果沒有符合條件的記錄
                            
                            frame_skip = 1  # 重置跳過幀的變數
                            break  # 退出內層循環以重新獲取幀
          
                except Exception as e:  
                    print(f"發生錯誤: {e}")  # 捕捉並打印任何異常
               
            
        def handle_keyboard_input(drone):
            while True:
                user_input = input("Enter your command: ")  # 等待用戶輸入
                # 處理用戶輸入的邏輯，例如更新 frame_skip 或其他變數
                print(f"User entered: {user_input}")
                    
                if user_input == "q":  # 如果輸入q，退出並停止無人機
                    drone.quit()
                    break
                if user_input == "1":
                    drone.takeoff()  # 無人機起飛
                    print("takeoff")
                    sleep(5)
                if user_input == "2":
                    drone.clockwise(25)  # 無人機順時針旋轉
                    print("clockwise")
                    sleep(4) # sleep(1): 10度?
                    drone.counter_clockwise(0)  # 停止旋轉
                    sleep(2)
                if user_input == "3":
                    drone.counter_clockwise(25)  # 無人機逆時針旋轉
                    print("counter_clockwise")
                    sleep(4)       
                    drone.clockwise(0)  # 停止旋轉                    
                    sleep(2)
                if user_input == "5":
                    drone.flip_back()  # 無人機翻轉
                    print("flip")
                    
                    sleep(2) 
                if user_input == "4":
                    drone.land()  # 無人機降落
                    print("land")
                    sleep(2)            
                
        drone = tellopy.Tello()
        try:
            drone.connect()  # 連接到無人機
            drone.wait_for_connection(60.0)  # 等待無人機的連接
        except Exception as ex:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)  # 捕捉並打印異常
            print(ex)  

        # 創建並啟動視頻處理執行緒
        video_thread = threading.Thread(target=process_video, args=(drone,))
        video_thread.start()
        
        # 創建並啟動鍵盤輸入處理執行緒
        keyboard_thread = threading.Thread(target=handle_keyboard_input, args=(drone,))
        keyboard_thread.start()
        
        # 等待兩個執行緒結束
        video_thread.join()
        keyboard_thread.join()
    else:
        print(f"無法連接到 {ssid}")

if __name__ == "__main__":
    #ssid = "TELLO-asiaunivdrone1"  # 替換為你想連接的SSID
    ssid = "TELLO-5A81DD"
    password = None  # 如果WiFi沒有密碼，將密碼設置為None
    connect_to_wifi(ssid, password)
                
# drone.up(25)
# sleep(2)
# drone.down(0)
# sleep(2)

# drone.down(25)
# sleep(2)
# drone.up(0)
# sleep(2)

# drone.forward(25)
# sleep(3)
# drone.backward(0)
# sleep(2)

# drone.backward(25)
# sleep(3)
# drone.forward(0)
# sleep(2)

# drone.right(25)
# sleep(

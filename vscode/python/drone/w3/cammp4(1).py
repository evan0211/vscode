import sys  
import traceback  
import tellopy  
import av  
import cv2  
import numpy as np  
from time import sleep  
import threading  

def process_video(drone):  
    retry = 30  
    container = None  
    while container is None and retry > 0:  
        retry -= 1  
        try:  
            container = av.open(drone.get_video_stream())  
        except av.AVError as ave:  
            print(f"Retrying video stream connection ({retry} attempts left): {ave}")
            sleep(1)  # 延遲以防止過快重試
  
    if container is None:
        print("Failed to connect to video stream.")
        return
  
    frame_skip = 300  
    img_use = 0  
    file_index = 1  
    out = None  
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4 編碼器
  
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
  
                if img_use == 1:  
                    # 初始化新的視頻文件
                    height, width, _ = image.shape  
                    out = cv2.VideoWriter(f'output_{file_index:03d}.mp4', fourcc, 30.0, (width, height))  
  
                # 將每一幀寫入當前的視頻文件  
                out.write(image)  
  
                if img_use >= 25:  
                    # 釋放當前文件並開始新的視頻文件  
                    out.release()  
                    img_use = 0  
                    file_index += 1
            else:
                continue
            break
  
    except av.AVError as e:  
        print(f"Error decoding video: {e}")  
    except Exception as e:  
        print(f"An unexpected error occurred: {e}")  
    finally:  
        if out is not None:  
            out.release()  
        print("Exiting video processing thread.")  
  
def handle_keyboard_input(drone):  
    while True:  
        user_input = input("Enter your command: ")  
        print(f"User entered: {user_input}")  
        if user_input == "q":  
            drone.quit()  
            break  
        elif user_input == "1":  
            drone.takeoff()  
            print("takeoff")  
            sleep(5)  
        elif user_input == "2":  
            drone.clockwise(25)  
            print("clockwise")  
            sleep(4)  
            drone.counter_clockwise(0)  
            sleep(2)  
        elif user_input == "3":  
            drone.counter_clockwise(25)  
            print("counter_clockwise")  
            sleep(4)  
            drone.clockwise(0)  
            sleep(2)  
        elif user_input == "5":  
            drone.flip_back()  
            print("flip")  
            sleep(2)  
        elif user_input == "4":  
            drone.land()  
            print("land")  
            sleep(2)  
  
drone = tellopy.Tello()  
try:  
    drone.connect()  
    drone.wait_for_connection(60.0)  
except Exception as ex:  
    print("Failed to connect to the drone.")
    traceback.print_exception(*sys.exc_info())  
    sys.exit(1)

# 創建並啟動視頻處理線程  
video_thread = threading.Thread(target=process_video, args=(drone,))  
video_thread.start()  
  
# 創建並啟動鍵盤輸入處理線程  
keyboard_thread = threading.Thread(target=handle_keyboard_input, args=(drone,))  
keyboard_thread.start()  
  
# 等待兩個線程結束  
video_thread.join()  
keyboard_thread.join()  
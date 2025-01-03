import os
import time
import cv2
import mediapipe as mp
from djitellopy import Tello
import threading

# 全域變數
exit_program = False
takeoff = False
lock = threading.Lock()  # 確保執行緒安全

# 處理鍵盤輸入的執行緒
def handle_input():
    global exit_program, takeoff
    while not exit_program:
        key = input("Enter command (t=takeoff, l=land, q=quit): ").strip().lower()
        with lock:
            if key == 't':  # 起飛
                takeoff = True
            elif key == 'l':  # 降落
                takeoff = False
            elif key == 'q':  # 退出程式
                exit_program = True
                break
            else:
                print("Invalid command. Use 't', 'l', or 'q'.")

# 自動連接到 Tello Wi-Fi
def connect_to_tello_wifi(ssid="TELLO-62B15E", retries=3):
    print("Connecting to Tello Wi-Fi...")
    for attempt in range(retries):
        if os.name == 'nt':  # Windows 系統
            os.system(f'netsh wlan connect name="{ssid}"')
        elif os.name == 'posix':  # macOS 或 Linux 系統
            os.system(f'nmcli dev wifi connect "{ssid}"')
        else:
            print("Your system does not support automatic Wi-Fi connection.")
            return False
        print(f"Attempt {attempt + 1} of {retries}. Waiting for connection...")
        time.sleep(5)
        return True
    return False

# 初始化 Tello
def initialize_tello():
    try:
        tello = Tello()
        tello.connect()
        print(f"Tello Connected! Battery: {tello.get_battery()}%")
        tello.streamon()  # 啟動視頻流
        return tello
    except Exception as e:
        print(f"Error initializing Tello: {e}")
        return None

# 主程式
def main():
    global exit_program, takeoff

    # 嘗試自動連接到 Tello Wi-Fi
    ssid = "TELLO-62B15E"  # Wi-Fi 名稱
    if not connect_to_tello_wifi(ssid):
        print("Failed to connect to Tello Wi-Fi.")
        return

    # 初始化 Tello
    tello = initialize_tello()
    if not tello:
        return

    # 初始化 MediaPipe Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        refine_landmarks=True,
        max_num_faces=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    mp_drawing = mp.solutions.drawing_utils

    # 啟動鍵盤輸入執行緒
    input_thread = threading.Thread(target=handle_input)
    input_thread.start()

    print("Camera is ready. Use commands: 't' to take off, 'l' to land, 'q' to quit.")
    flying = False

    try:
        while not exit_program:
            # 從 Tello 獲取攝像頭畫面
            frame = tello.get_frame_read().frame
            if frame is None:
                print("No frame received. Waiting...")
                continue

            # 將圖像轉為 RGB 格式
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 偵測臉部關鍵點
            results = face_mesh.process(rgb_frame)

            # 畫面資訊
            screen_height, screen_width, _ = frame.shape
            center_x, center_y = screen_width // 2, screen_height // 2

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    # 獲取鼻尖座標
                    nose = face_landmarks.landmark[1]
                    head_x = int(nose.x * screen_width)
                    head_y = int(nose.y * screen_height)

                    # 計算偏移量
                    offset_x = head_x - center_x
                    offset_y = head_y - center_y

                    # 顯示偏移量
                    cv2.putText(frame, f'Offset X: {offset_x}, Offset Y: {offset_y}', 
                                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.circle(frame, (head_x, head_y), 5, (0, 255, 0), -1)
                    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

                    # 若飛行中，根據偏移量調整 Tello 位置
                    if flying:
                        max_speed = 50
                        threshold = 30  # 減少靈敏度閾值
                        speed_x = int(offset_x / screen_width * max_speed)
                        speed_y = int(offset_y / screen_height * max_speed)

                        if abs(offset_x) > threshold:
                            tello.send_rc_control(speed_x, 0, 0, 0)

                        if abs(offset_y) > threshold:
                            tello.send_rc_control(0, 0, -speed_y, 0)
            else:
                cv2.putText(frame, 'No face detected!', (10, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # 顯示處理後的畫面
            cv2.imshow('Tello - Keep Head Centered', frame)

            # 控制 Tello 起飛並自動升高到 100 公分
            with lock:
                if takeoff and not flying:
                    print("Taking off and moving to 100cm height...")
                    tello.takeoff()
                    time.sleep(1)
                    tello.move_up(100)  # 快速上升到 100 公分
                    flying = True
                elif not takeoff and flying:
                    print("Landing...")
                    tello.land()
                    flying = False

            # 檢測是否退出程式
            if cv2.waitKey(1) & 0xFF == ord('q') or exit_program:
                break

    finally:
        # 結束程式，停止視頻流並降落
        if flying:
            tello.land()
        tello.streamoff()
        face_mesh.close()
        cv2.destroyAllWindows()
        print("Program terminated.")

# 執行主程式
if __name__ == "__main__":
    main()

import mediapipe as mp  
import cv2  
import os  
import sqlite3  
from datetime import datetime  
  
# 初始化 MediaPipe Hands 模組  
mp_hands = mp.solutions.hands  
hands = mp_hands.Hands(static_image_mode=False,  
                       max_num_hands=2,  
                       min_detection_confidence=0.5,  
                       min_tracking_confidence=0.5)  
  
# 初始化 MediaPipe 繪圖工具  
mp_drawing = mp.solutions.drawing_utils  

# SQLite 数据库文件路径  
db_file_path = './hand_detection.db'  
  
# 删除数据库文件（如果存在）  
if os.path.exists(db_file_path):  
    os.remove(db_file_path)  
  
# 创建 SQLite 数据库和表  
def create_table():  
    conn = sqlite3.connect(db_file_path)  
    cursor = conn.cursor()  
      
    # 清空表  
    cursor.execute('DROP TABLE IF EXISTS hand_detection')  
      
    # 创建表  
    cursor.execute('''  
        CREATE TABLE hand_detection (  
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            timestamp TEXT NOT NULL,  
            left_hand_position INTEGER NOT NULL,  
            right_hand_position INTEGER NOT NULL  
        )  
    ''')  
    conn.commit()  
    conn.close()  
  
create_table()  
  
def find_new_file(dir1, processed_files):  
    file_lists = os.listdir(dir1)  
    file_lists.sort(key=lambda fn: os.path.getmtime(os.path.join(dir1, fn))  
                    if not os.path.isdir(os.path.join(dir1, fn)) else 0)  
      
    # 找到未处理的文件  
    for file in file_lists:  
        file_path = os.path.join(dir1, file)  
        file_mtime = os.path.getmtime(file_path)  
          
        # 检查文件的修改时间是否在已处理文件中  
        if file not in processed_files or processed_files[file] < file_mtime:  
            return file_path, file, file_mtime  
      
    return None, None, None  # 如果没有新文件，返回 None  
  
# 存储已处理文件的字典，键为文件名，值为修改时间  
processed_files = {}  
  
while True:  
    try:  
        file, file2, file_mtime = find_new_file('./img', processed_files)  
  
        if file is None:  
            print("没有新文件可处理。")  
            continue  # 如果没有新文件，继续循环  
  
        # 读取图像并处理  
        color_image = cv2.imread(file)  
        image = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)  
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  
        # 进行手部检测  
        results = hands.process(image)  
  
        # 将图像转换回 BGR  
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  
  
        # 初始化位置  
        left_hand_position = 0  
        right_hand_position = 0  
  
        # 获取图像的高度  
        height, width, _ = image.shape  
  
        # 绘制手部关键点和连接线  
        if results.multi_hand_landmarks and results.multi_handedness:  # 检查手的类型  
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):  
                # 绘制关键点  
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)  
  
                # 判断左右手  
                hand_type = handedness.classification[0].label  
                 
                  
                # 计算手的中心位置  
                x_coords = [landmark.x * width for landmark in hand_landmarks.landmark]  
                y_coords = [landmark.y * height for landmark in hand_landmarks.landmark]  
                center_x = sum(x_coords) / len(x_coords)  
                center_y = sum(y_coords) / len(y_coords)  
  
                # 打印手的类型和中心位置  
                print(f"{timestamp}: {hand_type} 被检测到，中心位置: ({center_x}, {center_y})")  
  
                # 判断手的位置  
                if center_y < height / 2:  # 在上半部  
                    position = 1  
                else:  # 在下半部  
                    position = 0  
  
                # 更新位置  
                if hand_type == 'Left':  
                    left_hand_position = position  
                elif hand_type == 'Right':  
                    right_hand_position = position  
  
        # 将信息写入 SQLite 数据库  
        conn = sqlite3.connect(db_file_path)  
        cursor = conn.cursor()  
        cursor.execute('INSERT INTO hand_detection (timestamp, left_hand_position, right_hand_position) VALUES (?, ?, ?)',   
                       (timestamp, left_hand_position, right_hand_position))  
        conn.commit()  
        conn.close()  
  
        # 保存处理后的图像  
        cv2.imwrite(r'./img2/' + file2, image)  
  
        # 将文件标记为已处理，更新修改时间  
        processed_files[file2] = file_mtime  
  
    except Exception as e:  
        print(f"Sender stopped: {e}")  
  


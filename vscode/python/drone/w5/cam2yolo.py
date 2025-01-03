import cv2 
from ultralytics import YOLO
import time
model = YOLO("yolov10n.pt")
while True:
    file="img/1.jpg"
    image = cv2.imread(file) 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #
    results = model(file)
    result = results[0]
    boxes = result.boxes
    for box in boxes:        
        class_id = box.cls[0].item()
        print("Object type:", class_id)                   
        if class_id==0.0:
            print("person")
            cords = box.xyxy[0].tolist()        
            x1=cords[0]
            y1=cords[1]
            x2=cords[2]
            y2=cords[3]
            
            left = x1
            top = y1
            right = x2
            bottom = y2

            width = right - left
            height = bottom - top
            bbox = (int(left), int(top), int(width), int(height))
            
            person_img=image[int(bbox[1]):int(bbox[1] + bbox[3]), int(bbox[0]):int(bbox[0] + bbox[2]),:] # for jpg
            cv2.imwrite('./img2/1p.jpg', person_img)
    time.sleep(1)
                        
# # -*- coding: utf-8 -*-  
# import cv2 
# from ultralytics import YOLO

# model = YOLO("yolov10n.pt")

# # 攝像頭或視頻文件
# # 如果使用攝像頭，將 "video_source" 設為 0
# # 如果是視頻文件，則提供視頻文件的路徑，例如 "video_source = 'video.mp4'"
# video_source = 0

# cap = cv2.VideoCapture(video_source)

# while cap.isOpened():
#     ret, frame = cap.read()
    
#     if not ret:
#         print("未能讀取影像，結束程序。")
#         break
    
#     # 進行圖像轉換
#     frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
#     # 使用YOLO模型進行推論
#     results = model(frame)
#     result = results[0]
#     boxes = result.boxes
    
#     # 遍歷檢測到的物體框
#     for box in boxes:        
#         class_id = box.cls[0].item()
#         print("Object type:", class_id)                   
        
#         # 檢測到的人類 (通常 YOLO 的 class_id 0 表示人類)
#         if class_id == 0.0:
#             print("檢測到人")
#             cords = box.xyxy[0].tolist()        
#             x1, y1, x2, y2 = cords
            
#             # 計算邊界框的長寬
#             width = x2 - x1
#             height = y2 - y1
#             bbox = (int(x1), int(y1), int(width), int(height))
            
#             # 提取邊界框內的區域
#             person_img = frame[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2], :]
#             cv2.imwrite('./img2/1p.jpg', person_img)
    
#     # 顯示每幀處理的結果 (選擇性)
#     cv2.imshow('frame', frame)
    
#     # 按 'q' 鍵退出
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

# -*- coding: utf-8 -*-  

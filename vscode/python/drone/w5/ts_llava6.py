# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 15:03:04 2024

@author: udoo_w2
"""
from ollama import Client
client = Client(host='http://localhost:11434')
import os
import csv
import cv2
# Path to your video file
video_path = os.path.join('media2', 'move.mp4')
UPLOAD_FOLDER = 'img3'  
if not os.path.exists(UPLOAD_FOLDER):  
    os.makedirs(UPLOAD_FOLDER)  
    
# Create a VideoCapture object to read the video
cap = cv2.VideoCapture(video_path)

# Check if the video file opened successfully
if not cap.isOpened():    
    print("Error: Could not open video.")
    exit()

frame_count = 0
with open(UPLOAD_FOLDER+'.csv', mode='w', newline='', encoding='utf-8-sig') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['file', 'ans'])  # Write the header
    # Read frames in a loop
    while True:
        ret, frame = cap.read()  # Read one frame
        # # 取得影像的高度和寬度
        # height, width = frame.shape[:2]
    
        # # 上半部影像
        # upper_half = frame[:height // 2, :]
    
        # # 下半部影像
        # lower_half = frame[height // 2:, :]
        try:
            cv2.imwrite(UPLOAD_FOLDER+"/" + str(frame_count) + ".jpg", frame)
            res = client.chat(
                model="llava-phi3:latest",
                messages=[
                    {
                        'role':'user',
                        'content':"Is there a drone appearing in this image?",
                        'images':[UPLOAD_FOLDER+"/" + str(frame_count) + ".jpg"]
                        }
                    ]
                )
            ans=res['message']['content']
            #print(ans)
            if "Yes" in ans:                
                # Process each frame (for now, just show frame count)
                print(f"Processing frame {frame_count}")   
                print(ans)
                csv_writer.writerow([str(frame_count) + ".jpg", ans])
        except:
            if not ret:  # Check if the frame was not captured
                print("End of video or error occurred.")
                break  # Exit the loop if no frame is captured    
             
        
        frame_count += 1

# Release the capture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()



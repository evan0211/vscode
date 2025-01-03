# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 20:02:54 2024

@author: udoo_w2
"""
import mediapipe as mp
import cv2
import csv

# ====== Mediapipe ======
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

# Read the image and process it
color_image = cv2.imread(r'python\drone\4.jpg')
color_image_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)    

# Perform pose detection and draw the landmarks
with mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=True) as pose:
    results = pose.process(color_image_rgb)        

if results.pose_landmarks:        
    # Draw landmarks on the image
    mpDraw.draw_landmarks(color_image, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    
    # Prepare to save landmarks to a CSV file
    with open(r'python\drone\pose_landmarks.csv', mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['landmark', 'x', 'y', 'z'])  # Write the header
        
        # Write the landmarks data
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            csv_writer.writerow([idx, landmark.x, landmark.y, landmark.z])

# Display the result
cv2.namedWindow("mediapipe", cv2.WINDOW_AUTOSIZE)
cv2.imshow("mediapipe", color_image)
cv2.waitKey(0) 
cv2.imwrite("media/mp1.jpg", color_image)

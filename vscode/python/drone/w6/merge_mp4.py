# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 13:08:34 2024

@author: udoo_w2
"""
from moviepy.editor import VideoFileClip, concatenate_videoclips

# 載入多個 MP4 檔案
video_clips = [
    VideoFileClip("./2024_10_28_22_04_23/003.mp4"),
    VideoFileClip("./2024_10_28_22_04_23/004.mp4"),
    VideoFileClip("./2024_10_28_22_04_23/005.mp4")
]

# 合併所有影片
final_clip = concatenate_videoclips(video_clips)

# 將合併的影片儲存為新的 MP4 檔案
final_clip.write_videofile("merged_video.mp4", codec="libx264")

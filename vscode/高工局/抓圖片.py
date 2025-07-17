import cv2
import os
from datetime import datetime
import time


stream_url = "https://cctvc.freeway.gov.tw/abs2mjpg/bmjpg?camera=368"

SAVE_DIR = os.path.join("screenshots")
os.makedirs(SAVE_DIR, exist_ok=True)

while True:
    cap = cv2.VideoCapture(stream_url)

    ret, frame = cap.read()
    if ret:
        filename = datetime.now().strftime("camera436%Y%m%d_%H%M%S.jpg")
        filepath = os.path.join(SAVE_DIR, filename)
        cv2.imwrite(filepath, frame)
        print(f"✅ 成功擷取並儲存：{filepath}")
    else:
        print("❌ 讀取影像失敗")

    cap.release()
    time.sleep(300)
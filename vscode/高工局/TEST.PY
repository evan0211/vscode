import requests
import os
import time
from datetime import datetime
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_first_jpeg(url):
    with requests.get(url, headers=headers, stream=True, timeout=10, verify=False) as r:
        bytes_data = bytes()
        for chunk in r.iter_content(chunk_size=1024):
            bytes_data += chunk
            a = bytes_data.find(b'\xff\xd8')
            b = bytes_data.find(b'\xff\xd9')
            if a != -1 and b != -1:
                return bytes_data[a:b+2]
        return None

CAMERA_LIST = {
    "北 國道3號 220K+330 中興系統交流道到草屯交流道": "https://cctvc.freeway.gov.tw/abs2mjpg/bmjpg?camera=595",
    "南 國道3號 215K+319 霧峰系統交流道到草屯交流道": "https://cctvc.freeway.gov.tw/abs2mjpg/bmjpg?camera=276",
    "南 國道3號 218K+085": "https://cctvc.freeway.gov.tw/abs2mjpg/bmjpg?camera=1103",
    "南 國道3號 217K+091 草屯交流道到中興系統交流道": "https://cctvc.freeway.gov.tw/abs2mjpg/bmjpg?camera=277",
    "南 國道3號 219K+080 草屯交流道到中興系統交流道": "https://cctvc.freeway.gov.tw/abs2mjpg/bmjpg?camera=368",
    "南 國道3號 221K+536 草屯交流道到中興系統交流道": "https://cctvc.freeway.gov.tw/abs2mjpg/bmjpg?camera=369",
    

}

INTERVAL = 300
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "高工局影像")
os.makedirs(SAVE_DIR, exist_ok=True)


for name in CAMERA_LIST:
    os.makedirs(os.path.join(SAVE_DIR, name), exist_ok=True)
while True:
    print(f"\n 抓取時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for name, url in CAMERA_LIST.items():
        try:
            img = fetch_first_jpeg(url)
            if img:
                filename = datetime.now().strftime(f"{name}_%Y%m%d_%H%M%S.jpg")
                filepath = os.path.join(SAVE_DIR,name, filename)
                with open(filepath, 'wb') as f:
                    f.write(img)
                print(f"✅ 儲存成功：{filepath}")
            else:
                print(f"❌ 讀取失敗：{name}")
        except Exception as e:
            print(f"🚫 擷取失敗：{name}，錯誤：{e}")
    print(f"⏳ 等待 {INTERVAL} 秒...後再次抓取\n")
    time.sleep(INTERVAL)
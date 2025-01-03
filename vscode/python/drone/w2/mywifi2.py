# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:41:11 2024

@author: udoo_w2
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 13:11:26 2024

@author: udoo_w2
"""
import time
from pywifi import PyWiFi, const, Profile

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

    iface.remove_all_network_profiles()
    iface.add_network_profile(profile)
    iface.connect(profile)

    time.sleep(10)  # 等待連接

    if iface.status() == const.IFACE_CONNECTED:
        print(f"成功連接到 {ssid}")
    else:
        print(f"無法連接到 {ssid}")

if __name__ == "__main__":
    ssid = "TELLO-5A81DD"  # 替換為你想連接的SSID
    password = None  # 如果WiFi沒有密碼，將密碼設置為None
    connect_to_wifi(ssid, password)

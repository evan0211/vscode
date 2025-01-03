import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import matplotlib.pyplot as plt
import cv2
import os
import urllib
from PIL import Image 
import numpy as np
import matplotlib.pyplot as plt

driver = webdriver.Chrome()

driver.get("https://tixcraft.com/ticket/ticket/24_vashhsu/17286/1/94")
driver.maximize_window()
time.sleep(0.5)

captcha_element = driver.find_element(By.ID, 'TicketForm_verifyCode-image')
captcha_url = captcha_element.get_attribute('src')
response = requests.get(captcha_url)

local_path = 'images'
res = urllib.request.urlopen(captcha_url)
file_path = open(os.path.join(local_path , 't.jpg'),'wb')
size = 0
while True:
    info = res.read(10000)
    if len(info) < 1:
        break
    size = size + len(info)
    file_path.write(info)
print(f'已下載:',size)
file_path.close()
res.close()

imag = cv2.imread('./images/t.jpg')

kernel = np.ones((4,4), np.uint8)
erosion = cv2.erode(imag, kernel, iterations=1)
blurred = cv2.GaussianBlur(erosion, (5,5), 0)
edged = cv2.Canny(blurred,30,150)
dilation = cv2.dilate(edged,kernel,iterations=1)

contours, hierarchy = cv2.findContours(dilation.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key = lambda x:x[1])
ary = []
for (c,_) in cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    # print(x,y,w,h)
    if w>15 and h>15:
        ary.append((x,y,w,h))

fig = plt.figure()
for id, (x,y,w,h) in enumerate(ary):
    roi = dilation[y:y+h, x:x+w]
    thresh = roi.copy()
    a = fig.add_subplot(1,len(ary), id + 1)
    plt.imshow(thresh)
    plt.show()





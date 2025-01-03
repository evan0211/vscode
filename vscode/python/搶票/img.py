from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
from selenium.webdriver.common.keys import Keys
from tkinter import *
from tkinter import messagebox

from bs4 import BeautifulSoup as bs4
import requests

import json

import pytesseract
from PIL import Image

import ddddocr
import os
import numpy as np

ocr = ddddocr.DdddOcr()

driver = webdriver.Chrome()

driver.get("https://tixcraft.com/ticket/ticket/24_fireextp/16657/2/7")
time.sleep(0.5)

captcha_element = driver.find_element(By.ID, 'TicketForm_verifyCode-image')
captcha_url = captcha_element.get_attribute('src')
response = requests.get(captcha_url)
os.makedirs('images', exist_ok=True)

captcha_path = os.path.join('images', 'captcha_image.png')
with open(captcha_path, 'wb') as file:
    file.write(response.content)

with Image.open(captcha_path) as img:
    img = img.convert('RGB')
    img_array = np.array(img)
    print(f"图像形状: {img_array.shape}")

with open(captcha_path, 'rb') as image_file:
    image_bytes = image_file.read()
    result = ocr.classification(image_bytes)
print("验证码识别结果:", result)
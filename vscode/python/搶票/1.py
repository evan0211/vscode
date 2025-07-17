from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from selenium.webdriver.common.keys import Keys
from tkinter import *
from tkinter import messagebox
import json

def login():

    driver = webdriver.Chrome()  # 或你想用的瀏覽器驅動
    driver.get("https://tixcraft.com/activity/game/25_blackpink")  # 或是正確的活動網址
    
    onetrust = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    driver.execute_script("arguments[0].scrollIntoView(true);", onetrust)
    driver.execute_script("arguments[0].click();", onetrust)


#     cookie_string = '''tagHash=; _ga=GA1.1.334142479.1749490408; __gads=ID=fc891d276e345105:T=1749490408:RT=1749490408:S=ALNI_MbJ_hbUWEu_b_GRGGpHZ9H-yR_5Mg; __gpi=UID=00001127756da1eb:T=1749490408:RT=1749490408:S=ALNI_MYDEGQ3wt8cRPmb0eivJ2ObpGRE-Q; __eoi=ID=fa2b93a06c0c21b6:T=1749490408:RT=1749490408:S=AA-AfjYYdAvC9tFMGNdn_e4IAsq4; _ga_C3KRPGTSF6=GS2.1.s1749490408$o1$g1$t1749490417$j51$l0$h0; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jun+10+2025+01%3A33%3A40+GMT%2B0800+(%E5%8F%B0%E5%8C%97%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=202408.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=8afbfac4-6934-432f-bab6-33905986739c&interactionCount=1&isAnonUser=1&landingPath=https%3A%2F%2Ftixcraft.com%2Factivity%2Fdetail%2F25_valley&groups=C0001%3A1%2CC0003%3A0%2CC0002%3A0%2CC0004%3A0'''

# # 拆解 cookie 字串為 dict
#     driver.delete_all_cookies()
#     for item in cookie_string.split('; '):
#         if '=' in item:
#             name, value = item.split('=', 1)
#             cookie_dict = {
#                 'name': name,
#                 'value': value,
#                 'domain': 'https://tixcraft.com/activity/game/25_blackpink',   # ⚠️ 很重要
#                 'path': '/',
#             }
#             try:
#                 driver.add_cookie(cookie_dict)
#             except Exception as e:
#                 print(f"無法加入 cookie {name}: {e}")

# # 重新整理，cookie 就生效了
#     driver.refresh()



    


    target_time = datetime.datetime(2025, 6, 10, 11, 00)
    
    while datetime.datetime.now() < target_time:
        time.sleep(1)
    #按立即訂購
    driver.refresh()
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/section[2]/div/div[2]/div[2]/table/tbody/tr/td[4]/button")))
    driver.execute_script("arguments[0].scrollIntoView(true);", button) 
    driver.execute_script("arguments[0].click();", button) 

    time.sleep(1)
    
    #選座位
    seat = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH , "/html/body/div[2]/div[1]/div[3]/div/div/div/div[2]/div[2]/ul[1]/li/a/font")))
    driver.execute_script("arguments[0].scrollIntoView(true);", seat) 
    driver.execute_script("arguments[0].click();", seat) 

    #選擇人數
    select = Select(driver.find_element(By.NAME , "TicketForm[ticketPrice][01]")) 
    select.select_by_value('2') 

    #勾同意
    check = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "TicketForm_agree")))
    driver.execute_script("arguments[0].scrollIntoView(true);", check)
    driver.execute_script("arguments[0].click();", check)

    wait_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "TicketForm_verifyCode")))
    driver.execute_script("arguments[0].scrollIntoView(true);", wait_input)
    driver.execute_script("arguments[0].click();", wait_input)

    time.sleep(100)

login()
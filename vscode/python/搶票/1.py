from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
from selenium.webdriver.common.keys import Keys
from tkinter import *
from tkinter import messagebox

driver = webdriver.Chrome()

driver.get("https://tixcraft.com/")
time.sleep(0.5)


img = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))



# 接受cookie
cookie = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
cookie.click()

choose = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "滅火器 Fire EX.《一生到底 One Life， One Shot》演唱會 - 台北場")))
driver.execute_script("arguments[0].scrollIntoView(true);", choose)
driver.execute_script("arguments[0].click();", choose)

#按立即購票
#按立即購票
open_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.buy a")))
driver.execute_script("arguments[0].scrollIntoView(true);", open_button)
driver.execute_script("arguments[0].click();", open_button)


#按立即訂購
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.text-bold.m-0[data-href='https://tixcraft.com/ticket/area/24_fireextp/16657']")))
driver.execute_script("arguments[0].scrollIntoView(true);", button) 
driver.execute_script("arguments[0].click();", button) 

# #選座位
# seat = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID , "16987_2")))
# driver.execute_script("arguments[0].scrollIntoView(true);", seat) 
# driver.execute_script("arguments[0].click();", seat) 

# #選擇人數
# select = Select(driver.find_element(By.NAME , "TicketForm[ticketPrice][03]")) 
# select.select_by_value('1') 

# #勾同意
# check = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "TicketForm_agree")))
# driver.execute_script("arguments[0].scrollIntoView(true);", check)
# driver.execute_script("arguments[0].click();", check)

# #確認張數
# confirm = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.btn-green")))
# driver.execute_script("arguments[0].scrollIntoView(true);", confirm)
# driver.execute_script("arguments[0].click();", confirm)


# time.sleep(3)






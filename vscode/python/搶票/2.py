from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
from selenium.webdriver.common.keys import Keys
from tkinter import *
from tkinter import messagebox

def login():

    driver = webdriver.Chrome()  # 或你想用的瀏覽器驅動
    driver.get("https://ticket-training.onrender.com/")  # 或是正確的活動網址

 
    # #選場次
    # choose = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "thumb-shadow")))
    # driver.execute_script("arguments[0].scrollIntoView(true);", choose)
    # driver.execute_script("arguments[0].click();", choose)

    
    
    confirmRead = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "confirmRead")))
    driver.execute_script("arguments[0].scrollIntoView(true);", confirmRead)
    driver.execute_script("arguments[0].click();", confirmRead)
    closeModal = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "closeModal")))
    driver.execute_script("arguments[0].scrollIntoView(true);", closeModal)
    driver.execute_script("arguments[0].click();", closeModal)

    input_box = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "countdownInput")))
    input_box.clear()
    input_box.send_keys("1")
    
    startButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "startButton")))
    driver.execute_script("arguments[0].scrollIntoView(true);", startButton)
    driver.execute_script("arguments[0].click();", startButton)
    time.sleep(1)
    #按立即購票
    open_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "active")))
    driver.execute_script("arguments[0].scrollIntoView(true);", open_button)
    driver.execute_script("arguments[0].click();", open_button)


    #按立即訂購
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "purchase-button")))
    driver.execute_script("arguments[0].scrollIntoView(true);", button) 
    driver.execute_script("arguments[0].click();", button) 


    input_box = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "memberId")))
    input_box.clear()
    input_box.send_keys("1")

    button1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME , "submit-button")))
    driver.execute_script("arguments[0].scrollIntoView(true);", button1) 
    driver.execute_script("arguments[0].click();", button1) 
    
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    #選座位
    seat = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME , "seat-item")))
    driver.execute_script("arguments[0].scrollIntoView(true);", seat) 
    driver.execute_script("arguments[0].click();", seat) 

    #選擇人數
    select = Select(driver.find_element(By.CLASS_NAME , "quantity-select")) 
    select.select_by_value('2') 

    #勾同意
    check = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "terms-checkbox")))
    driver.execute_script("arguments[0].scrollIntoView(true);", check)
    driver.execute_script("arguments[0].click();", check)

    wait_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "TicketForm_verifyCode")))
    driver.execute_script("arguments[0].scrollIntoView(true);", wait_input)
    driver.execute_script("arguments[0].click();", wait_input)
    time.sleep(10)


    #確認張數
    confirm = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.btn-green")))
    driver.execute_script("arguments[0].scrollIntoView(true);", confirm)
    driver.execute_script("arguments[0].click();", confirm)

    # time.sleep(10)
    # driver.quit()

login()
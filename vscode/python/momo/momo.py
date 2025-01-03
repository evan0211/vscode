from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
driver = webdriver.Chrome()
driver.get("https://www.momoshop.com.tw/edm/cmmedm.jsp?lpn=O5hDiZNxMpo&n=1&mdiv=1099900000-bt_0_247_01-bt_0_247_01_P1_2_e1&ctype=B")
time.sleep(0.5)

    

login = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR , "img#regImgPhone_0.js-REG_reglmg_phone.lazy.lazy-loaded")))
driver.execute_script("arguments[0].scrollIntoView(true);", login)
driver.execute_script("arguments[0].click();", login)
# time.sleep(10)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://thisav.com/actresses/ranking")
time.sleep(0.5)

# 定义一个字典来存储演员及其对应的 AV 编号
av_data = {}

# 获取所有要点击的元素
elements = driver.find_elements(By.CSS_SELECTOR, ".text-nord13.truncate")
links = driver.find_elements(By.CSS_SELECTOR, "a.text-nord13")

# 遍历所有元素
for i in range(len(elements)):
    # 获取演员名字
    actor_name = elements[i].text
    av_data[actor_name] = []  # 初始化每个演员的 AV 列表
    
    # 获取演员的链接
    driver = webdriver.Chrome()
    actor_link = links[4+(2*i)].get_attribute('href')  # 从链接元素中获取 href 属性
    driver.get(actor_link)  # 跳转到演员的页面

    # 获取该演员的 AV 编号
    x = driver.find_elements(By.CSS_SELECTOR, ".text-secondary.group-hover\\:text-primary")
    y = []  # 每次循环初始化 y

    # 遍历 x 中的每个元素，将其文本添加到 y 列表中
    for j in x:
        y.append(j.text)
    
    # 将 AV 编号添加到演员的字典中
    av_data[actor_name] = y
    driver.quit()
    print(av_data)

# 输出所有收集的数据
for actor, movies in av_data.items():
    print(f'"{actor}": {movies},')

time.sleep(10)
# driver.quit()

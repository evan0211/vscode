from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
from selenium.webdriver.common.keys import Keys
from tkinter import *
from tkinter import messagebox

def ticket():
    window = Tk()
    window.title("搶票帳號輸入")
    window.geometry("270x140")
    
    #登入FB帳密
    top_text = Label(window,text="登入FB帳密",font=("Arial",20,"bold"))
    top_text.grid(row=0,column=0,columnspan=2)
    
    #輸入FB帳號
    login_email_text = Label(window,text="輸入FB帳號: ")
    login_email_text.grid(row=1,column=0)

    #密碼輸入
    login_email_input = Entry(window,width=25)
    login_email_input.grid(row=1,column=1)

    #輸入FB密碼
    login_password_text = Label(window,text="輸入FB密碼: ")
    login_password_text.grid(row=2,column=0)
    
    #帳號輸入
    login_password_input = Entry(window,width=25,show="*")
    login_password_input.grid(row=2,column=1)

    #判斷帳密是否有輸入
    def if_login_error():
        email = login_email_input.get()
        password = login_password_input.get() 
        if not email or not password:
            error()
        else:
            login(login_email_input,login_password_input,window)
            window.destroy
    #報錯框
    def error():
        messagebox.showerror("輸入錯誤", "帳號或密碼沒有輸入")
        login_email_input.delete(0,END)
        login_password_input.delete(0,END)

    run_button = Button(window,width=10 ,text="run",command=if_login_error)
    run_button.grid(row=3,pady=10,columnspan=2)

    window.mainloop()


def login(login_email_input,login_password_input,window):

    #報錯框
    def login_error():
        messagebox.showerror("輸入錯誤" , "帳號或密碼錯誤")
        driver.quit()
    
    email = login_email_input.get()
    password = login_password_input.get()
        
    driver = webdriver.Chrome()
    driver.get("https://tixcraft.com/")
    time.sleep(0.5)
    
    #同意cookie
    cookie = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID , "onetrust-accept-btn-handler")))
    driver.execute_script("arguments[0].click();", cookie)     

    #登入會員
    login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR , "a.justify-content-center")))
    driver.execute_script("arguments[0].scrollIntoView(true);", login)
    driver.execute_script("arguments[0].click();", login)

    #選擇fb登入
    loginFacebook = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "loginFacebook")))
    driver.execute_script("arguments[0].scrollIntoView(true);", loginFacebook)
    driver.execute_script("arguments[0].click();", loginFacebook)

    #輸入帳號
    send_email = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "email")))
    send_email.send_keys(email)

    #輸入密碼
    send_password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "pass")))
    send_password.send_keys(password)

    #登入
    loginbutton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "loginbutton")))
    driver.execute_script("arguments[0].scrollIntoView(true);", loginbutton )
    driver.execute_script("arguments[0].click();", loginbutton )

    #以...身分繼續
    continue_login = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.x6s0dn4.x78zum5.xl56j7k.x1608yet.xljgi0e.x1e0frkt")))
    driver.execute_script("arguments[0].scrollIntoView(true);", continue_login )
    driver.execute_script("arguments[0].click();", continue_login )
    
    try:
    #選場次
        choose = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, "thumb-shadow")))
        driver.execute_script("arguments[0].scrollIntoView(true);", choose)
        driver.execute_script("arguments[0].click();", choose)
    except:
        login_error()  

    #按立即購票
    open_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.buy a")))
    driver.execute_script("arguments[0].scrollIntoView(true);", open_button)
    driver.execute_script("arguments[0].click();", open_button)


    #按立即訂購
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.text-bold.m-0[data-href='https://tixcraft.com/ticket/area/24_jpleaders/16859']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", button) 
    driver.execute_script("arguments[0].click();", button) 
    
    #選座位
    seat = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID , "16859_2")))
    driver.execute_script("arguments[0].scrollIntoView(true);", seat) 
    driver.execute_script("arguments[0].click();", seat) 

    #選擇人數
    select = Select(driver.find_element(By.NAME , "TicketForm[ticketPrice][01]")) 
    select.select_by_value('1') 

    #勾同意
    check = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "TicketForm_agree")))
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

    time.sleep(10)
    # driver.quit()

ticket()
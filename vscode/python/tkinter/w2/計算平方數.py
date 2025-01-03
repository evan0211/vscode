from tkinter import *
from tkinter import messagebox

window = Tk()
window.title("計算平方數")
window.geometry("180x140")

top_text = Label(window, text="計算平方數", font=("Arial", 20, "bold"))
top_text.grid(row=0, column=0, columnspan=2)

login_email_input = Entry(window, width=25)
login_email_input.grid(row=1, column=1)

def error():
    messagebox.showerror("輸入錯誤", "請輸入有效的數字")

def if_login_error():
    email = login_email_input.get()  
    try:
        num = float(email)  
        square = num ** 2  
        result_label.config(text=f"平方數: {square}")
    except ValueError:
        error()  

run_button = Button(window, width=10, text="計算", command=if_login_error)
run_button.grid(row=3, pady=10, columnspan=2)

result_label = Label(window, text="", font=("Arial", 14))
result_label.grid(row=4, column=0, columnspan=2)

window.mainloop()
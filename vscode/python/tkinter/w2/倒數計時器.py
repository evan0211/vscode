
from tkinter import *

win = Tk()
win.title("ch2_23")


login_email_input = Entry(win, width=25)
login_email_input.grid(row=1, column=1)


digit = Label(win, text="", font=("Arial", 20, "bold"))
digit.grid(row=2, column=1)


def run_counter():
    try:
        
        counter = int(login_email_input.get())
        
        def counting():
            nonlocal counter
            if counter > 0:
                counter -= 1
                digit.config(text=str(counter))
                digit.after(1000, counting)  
            else:
                digit.config(text="計數完成")
        
        counting()  
    except ValueError:
        digit.config(text="請輸入有效的數字")  
run_button = Button(win, width=10, text="開始", command=run_counter)
run_button.grid(row=3, pady=10, columnspan=2)
win.mainloop()
from tkinter import *
from tkinter import messagebox

win = Tk()
win.title("質數檢查器")
win.geometry("300x200")

Label(win, text="請輸入一個數字:").grid(row=0, column=0, padx=10, pady=10)
number_input = Entry(win, width=10)
number_input.grid(row=0, column=1)

result_label = Label(win, text="", font=("Arial", 12))
result_label.grid(row=2, column=0, columnspan=2, pady=10)

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def check_prime():
    try:
        num = int(number_input.get())
        if is_prime(num):
            result_label.config(text=f"{num} 是質數")
        else:
            result_label.config(text=f"{num} 不是質數")
    except ValueError:
        messagebox.showerror("輸入錯誤", "請輸入有效的整數")

check_button = Button(win, text="檢查", command=check_prime)
check_button.grid(row=1, column=0, columnspan=2, pady=10)

win.mainloop()

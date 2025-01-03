from tkinter import *
from tkinter import messagebox

win = Tk()
win.title("密碼驗證表單")
win.geometry("300x150")


Label(win, text="請輸入密碼:").grid(row=0, column=0, pady=10, padx=10)
password_input1 = Entry(win, show="*", width=20)
password_input1.grid(row=0, column=1)

Label(win, text="請再次輸入密碼:").grid(row=1, column=0, pady=10, padx=10)
password_input2 = Entry(win, show="*", width=20)
password_input2.grid(row=1, column=1)


def check_password():
    password1 = password_input1.get()
    password2 = password_input2.get()

    if password1 == password2:
        messagebox.showinfo("結果", "密碼匹配！")
    else:
        messagebox.showerror("錯誤", "兩次輸入的密碼不一致！")


submit_button = Button(win, text="提交", command=check_password)
submit_button.grid(row=2, column=0, columnspan=2, pady=20)


win.mainloop()

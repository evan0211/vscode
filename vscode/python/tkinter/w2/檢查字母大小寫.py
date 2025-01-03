from tkinter import *
from tkinter import messagebox

win = Tk()
win.title("字母檢查器")
win.geometry("400x250")

Label(win, text="請輸入一段文字:").grid(row=0, column=0, padx=10, pady=10)
text_input = Entry(win, width=30)
text_input.grid(row=0, column=1)

uppercase_label = Label(win, text="大寫字母數: 0", font=("Arial", 12))
uppercase_label.grid(row=2, column=0, columnspan=2, pady=10)

lowercase_label = Label(win, text="小寫字母數: 0", font=("Arial", 12))
lowercase_label.grid(row=3, column=0, columnspan=2, pady=10)

def check_letters():
    text = text_input.get()  
    uppercase_count = 0
    lowercase_count = 0

    for char in text:
        if char.isupper():
            uppercase_count += 1
        elif char.islower():
            lowercase_count += 1
    
    uppercase_label.config(text=f"大寫字母數: {uppercase_count}")
    lowercase_label.config(text=f"小寫字母數: {lowercase_count}")

check_button = Button(win, text="檢查", command=check_letters)
check_button.grid(row=1, column=0, columnspan=2, pady=10)

win.mainloop()

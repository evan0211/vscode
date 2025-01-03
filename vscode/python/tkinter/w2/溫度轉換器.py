from tkinter import *
from tkinter import messagebox


win = Tk()
win.title("華氏轉攝氏溫度轉換器")
win.geometry("300x150")


Label(win, text="請輸入華氏溫度:").grid(row=0, column=0, padx=10, pady=10)
fahrenheit_input = Entry(win, width=10)
fahrenheit_input.grid(row=0, column=1)


result_label = Label(win, text="")
result_label.grid(row=2, column=0, columnspan=2, pady=10)


def convert_temperature():
    try:
        fahrenheit = float(fahrenheit_input.get())
        celsius = (fahrenheit - 32) * 5 / 9
        result_label.config(text=f"攝氏溫度: {celsius:.2f}°C")
    except ValueError:
        messagebox.showerror("輸入錯誤", "請輸入有效的數字")


convert_button = Button(win, text="轉換", command=convert_temperature)
convert_button.grid(row=1, column=0, columnspan=2, pady=10)


win.mainloop()

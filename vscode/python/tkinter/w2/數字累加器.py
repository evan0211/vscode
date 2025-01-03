from tkinter import *
from tkinter import messagebox


win = Tk()
win.title("累加器")
win.geometry("300x200")


total_sum = 0


Label(win, text="請輸入數字:").grid(row=0, column=0, padx=10, pady=10)
number_input = Entry(win, width=10)
number_input.grid(row=0, column=1)

sum_label = Label(win, text=f"當前總和: {total_sum}", font=("Arial", 12))
sum_label.grid(row=2, column=0, columnspan=2, pady=10)

def add_to_sum():
    global total_sum
    try:
        num = float(number_input.get())
        total_sum += num
        sum_label.config(text=f"當前總和: {total_sum:.2f}")
        number_input.delete(0, END)
    except ValueError:
        messagebox.showerror("輸入錯誤", "請輸入有效的數字")


add_button = Button(win, text="加入", command=add_to_sum)
add_button.grid(row=1, column=0, columnspan=2, pady=10)


win.mainloop()

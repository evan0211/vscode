from tkinter import *


win = Tk()
win.title("費氏數列生成器")
win.geometry("400x300")


Label(win, text="請輸入一個數字 n:").grid(row=0, column=0, pady=10, padx=10)
number_input = Entry(win, width=10)
number_input.grid(row=0, column=1)


result_label = Label(win, text="", wraplength=350, justify=LEFT)
result_label.grid(row=2, column=0, columnspan=2, pady=10)


def generate_fibonacci():

        n = int(number_input.get())  
        if n <= 0:
            result_label.config(text="請輸入一個正整數。")
            return
        
       
        fibonacci_sequence = []
        a, b = 0, 1
        for i in range(n):
            fibonacci_sequence.append(a)
            a, b = b, a + b
        
      
        result_label.config(text=f"前 {n} 項費氏數列: {', '.join(map(str, fibonacci_sequence))}")
    



generate_button = Button(win, text="生成數列", command=generate_fibonacci)
generate_button.grid(row=1, column=0, columnspan=2, pady=10)


win.mainloop()

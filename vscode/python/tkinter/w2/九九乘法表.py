from tkinter import *
win = Tk()
for i in range(1, 10):
    for j in range(1, 10):
        a = Label(win, text=f'{i}x{j}={i*j}')
        a.grid(column=i, row=j) 
win.mainloop()


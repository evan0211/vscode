from tkinter import *
from math import sqrt, sin, cos, tan, log
win = Tk()
win.title("計算機")
win.geometry("285x170")
win.configure(bg="gray")

def calculate():
    try:
        result = eval(i.get())
        i.set(i.get())
        result_label.config(text=f'={result}')
    except Exception:
        i.set("錯誤")
def show(buttonstring):
    i.set( i.get()+ buttonstring)
def clear():
    i.set("")
    result_label.config(text="")
def backspace():
    i.set(i.get()[:-1])
def x():
    i.set(f"1/{i.get()}")


i = StringVar()
i.set("")

Label(win, width=40, height=1, bg="black", anchor="ne", fg="white", textvariable=i).grid(row=0, column=0, columnspan=6, padx=1)
result_label = Label(win, width=40, height=1, bg="black", anchor="ne", fg="white")
result_label.grid(row=1, column=0, columnspan=6, padx=1)
Button(win, text="abs", width=5, height=1, bg="gainsboro", command=lambda:show("abs(")).grid(row=2, column=0, padx=1)
Button(win, text="sin", width=5, height=1, bg="gainsboro", command=lambda:show("sin(")).grid(row=3, column=0, padx=1)
Button(win, text="cos", width=5, height=1, bg="gainsboro", command=lambda:show("cos(")).grid(row=4, column=0, padx=1)
Button(win, text="tan", width=5, height=1, bg="gainsboro", command=lambda:show("tan(")).grid(row=5, column=0, padx=1)
Button(win, text="log", width=5, height=1, bg="gainsboro", command=lambda:show("log(")).grid(row=6, column=0, padx=1)

Button(win, text="sqrt", width=5, height=1, bg="gainsboro", command=lambda:show("sqrt(")).grid(row=2, column=1, padx=1)
Button(win, text="1/x", width=5, height=1, bg="gainsboro", command=x).grid(row=3, column=1, padx=1)
Button(win, text="x^y", width=5, height=1, bg="gainsboro", command=lambda:show("**")).grid(row=4, column=1, padx=1)
Button(win, text="(", width=5, height=1, bg="gainsboro", command=lambda:show("(")).grid(row=5, column=1, padx=1)
Button(win, text=")", width=5, height=1, bg="gainsboro", command=lambda:show(")")).grid(row=6, column=1, padx=1)

Button(win, text="C", width=5, height=1, bg="gainsboro", command=clear).grid(row=2, column=2, padx=1)
Button(win, text="7", width=5, height=1, bg="gainsboro", command=lambda:show("7")).grid(row=3, column=2, padx=1)
Button(win, text="4", width=5, height=1, bg="gainsboro", command=lambda:show("4")).grid(row=4, column=2, padx=1)
Button(win, text="1", width=5, height=1, bg="gainsboro", command=lambda:show("1")).grid(row=5, column=2, padx=1)

Button(win, text="DEL", width=5, height=1, bg="gainsboro", command=backspace).grid(row=2, column=3, padx=1)
Button(win, text="8", width=5, height=1, bg="gainsboro", command=lambda:show("8")).grid(row=3, column=3, padx=1)
Button(win, text="5", width=5, height=1, bg="gainsboro", command=lambda:show("5")).grid(row=4, column=3, padx=1)
Button(win, text="2", width=5, height=1, bg="gainsboro", command=lambda:show("2")).grid(row=5, column=3, padx=1)

Button(win, text="0", width=12, height=1, bg="gainsboro", command=lambda:show("0")).grid(row=6, column=2, columnspan=2, padx=1)

Button(win, text="%", width=5, height=1, bg="gainsboro", command=lambda:show("/100")).grid(row=2, column=4, padx=1)
Button(win, text="9", width=5, height=1, bg="gainsboro", command=lambda:show("9")).grid(row=3, column=4, padx=1)
Button(win, text="6", width=5, height=1, bg="gainsboro", command=lambda:show("6")).grid(row=4, column=4, padx=1)
Button(win, text="3", width=5, height=1, bg="gainsboro", command=lambda:show("3")).grid(row=5, column=4, padx=1)
Button(win, text=".", width=5, height=1, bg="gainsboro", command=lambda:show(".")).grid(row=6, column=4, padx=1)

Button(win, text="/", width=5, height=1, bg="gainsboro", command=lambda:show("/")).grid(row=2, column=5, padx=1)
Button(win, text="*", width=5, height=1, bg="gainsboro", command=lambda:show("*")).grid(row=3, column=5, padx=1)
Button(win, text="-", width=5, height=1, bg="gainsboro", command=lambda:show("-")).grid(row=4, column=5, padx=1)
Button(win, text="+", width=5, height=1, bg="gainsboro", command=lambda:show("+")).grid(row=5, column=5, padx=1)
Button(win, text="=", width=5, height=1, bg="gainsboro", command=calculate).grid(row=6, column=5, padx=1)



win.mainloop()
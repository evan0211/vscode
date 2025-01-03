from tkinter import *
win = Tk()
win.title("Loan Calculator")
win.geometry("500x600")

def toggle_early_repayment():
    if var.get():
        early_repayment_amount.config(state=NORMAL)
        early_repayment_time.config(state=NORMAL)
    else:
        early_repayment_amount.config(state=DISABLED)
        early_repayment_time.config(state=DISABLED)
def calculate():
    months_rate = int(interest_rate.get())/1200
    months = int(years.get())*12
    payment= int(money.get())

    monthly_payment = (payment * months_rate) / (1 - (1 + months_rate) ** -months)
    monthly_money.config(text=int(monthly_payment)) 

    result_text = "月份\t本金還款\t\t利息還款\t\t剩餘本金\n"

    if var.get():
        early_repayment_money = int(early_repayment_amount.get())
        early_repayment_month = int(early_repayment_time.get())
    for month in range(1, months + 1):
        
        lastpayment = payment
        interest_payment = payment * months_rate
        month_payment = monthly_payment - interest_payment
        if  var.get() and month == early_repayment_month:
            month_payment = early_repayment_money
            payment -= early_repayment_money
            monthly_payment = (payment * months_rate) / (1 - (1 + months_rate) ** -(months-month))
            early_repaymentLabel_monthly_money.config(text=int(monthly_payment)) 
        else:
            payment -=  month_payment
        if month == months:
            result_text += f"{month}\t{lastpayment-interest_payment:.0f}\t\t{interest_payment:.0f}\t\t0\n"
        else:
            result_text += f"{month}\t{month_payment:.0f}\t\t{interest_payment:.0f}\t\t{payment:.0f}\n"


    result.delete(1.0, END)
    result.insert(END, result_text)
    
def clear():
    interest_rate.delete(0, END)
    years.delete(0, END)
    money.delete(0, END)
    var.set(0)
    early_repayment_amount.delete(0, END)
    early_repayment_time.delete(0, END)
    early_repayment_amount.config(state=DISABLED)
    early_repayment_time.config(state=DISABLED)
    monthly_money.config(text="")
    early_repaymentLabel_monthly_money .config(text="")
    result.delete(1.0, END)
    

Label(win, text="貸款年利率(%):", width=20, anchor="w").grid(row=0, column=0, sticky="w")
Label(win, text="貸款年數:", width=20, anchor="w").grid(row=1, column=0, sticky="w")
Label(win, text="貸款金額:", width=20, anchor="w").grid(row=2, column=0, sticky="w")
Label(win, text="提前還款:", width=20, anchor="w").grid(row=3, column=0, sticky="w")
Label(win, text="提前還款時間(月數):", width=20, anchor="w").grid(row=4, column=0, sticky="w")
Label(win, text="提前還款金額:", width=20, anchor="w").grid(row=5, column=0, sticky="w")
Label(win, text="提前還款前月付款:", width=20, anchor="w").grid(row=6, column=0, sticky="w")
Label(win, text="提前還款後月付款:", width=20, anchor="w").grid(row=7, column=0, sticky="w")

interest_rate = Entry(win, width=20, justify="right")
interest_rate.grid(row=0, column=2, sticky="w")
years = Entry(win, width=20, justify="right")
years.grid(row=1, column=2, sticky="w")
money = Entry(win, width=20, justify="right")
money.grid(row=2, column=2, sticky="w")
var = IntVar()
early_repayment_check = Checkbutton(win, variable=var, command=toggle_early_repayment)
early_repayment_check.grid(row=3, column=1, sticky="e")
early_repayment_time = Entry(win, width=20, justify="right", state=DISABLED)
early_repayment_time.grid(row=4, column=2, sticky="w")
early_repayment_amount = Entry(win, width=20, justify="right", state=DISABLED)
early_repayment_amount.grid(row=5, column=2, sticky="w")
monthly_money = Label(win, text="", width=20)
monthly_money.grid(row=6, column=2, sticky="w")
early_repaymentLabel_monthly_money = Label(win, text="", width=20)
early_repaymentLabel_monthly_money.grid(row=7, column=2, sticky="w")

calculate_btn = Button(win, text="計算貸款金額", command=calculate)
calculate_btn.grid(row=8, column=2, columnspan=2, pady=5 )
clear_btn = Button(win, text="清除", command=clear)
clear_btn.grid(row=8, column=3, pady=5)
result = Text(win, height=20, width=70)
result.grid(row=9, columnspan=4)






win.mainloop()


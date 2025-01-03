from tkinter import *
from tkinter.ttk import *
import matplotlib.pyplot as plt

win = Tk()
win.title("Loan Calculator")
win.geometry("700x600")

updating = False  

def fill(*args):
    global updating
    if not updating: 
        updating = True
        Eyear.delete(0, END)
        Eyear.insert(0, f"{mslider.get():.0f}")
        Eloan.delete(0, END)
        Eloan.insert(0, f"{rslider.get():.0f}")
        Erate.delete(0, END)
        Erate.insert(0, f"{lslider.get():.1f}")
        updating = False


def update_slider_from_entry(*args):
    global updating
    if not updating:
        try:
            updating = True
 
            if Eyear.get().isdigit() and 0 <= int(Eyear.get()) <= 100:
                mslider.set(int(Eyear.get()))
            

            if Eloan.get().isdigit() and 0 <= int(Eloan.get()) <= 100000000:
                rslider.set(int(Eloan.get()))
            

            if Erate.get().replace('.', '', 1).isdigit():
                rate = float(Erate.get())
                if 0 <= rate <= 20:
                    lslider.set(rate)
        except ValueError:
            pass  
        finally:
            updating = False





def toggle_early_repayment():

    if var.get():
        early_repayment_amount.config(state=NORMAL)
        early_repayment_time.config(state=NORMAL)
    else:
        early_repayment_amount.config(state=DISABLED)
        early_repayment_time.config(state=DISABLED)


def cal():
    clear()
    term = []
    ins = []
    prin = []
    months_rate = float(interest_rate.get()) / 1200
    months = int(years.get()) * 12
    payment = int(money.get())

    monthly_payment = (payment * months_rate) / (1 - (1 + months_rate) ** -months)
    monthly_money.config(text=f"{monthly_payment:.2f}")
    result_text = "月份\t本金還款\t\t利息還款\t\t剩餘本金\n"

    if var.get():
        early_repayment_money = int(early_repayment_amount.get())
        early_repayment_month = int(early_repayment_time.get())

    for month in range(1, months + 1):
        interest_payment = payment * months_rate
        month_payment = monthly_payment - interest_payment
        term.append(month)
        ins.append(interest_payment)
        prin.append(month_payment)

        if var.get() and month == early_repayment_month:
            month_payment = early_repayment_money
            payment -= early_repayment_money
            monthly_payment = (payment * months_rate) / (1 - (1 + months_rate) ** -(months - month))
            early_repaymentLabel_monthly_money.config(text=f"{monthly_payment:.2f}")
        else:
            payment -= month_payment

        result_text += f"{month}\t{month_payment:.0f}\t\t{interest_payment:.0f}\t\t{payment:.0f}\n"

    plt.clf()
    plt.plot(term, ins,prin)
    plt.legend(['interest','principal'])
    plt.xlabel("months")
    plt.ylabel("NTD dollars")
    plt.show()

    result.delete(1.0, END)
    result.insert(END, result_text)


def cal2():
    clear()
    term = []
    ins = []
    prin = []
    months_rate = float(interest_rate.get()) / 1200
    months = int(years.get()) * 12
    payment = int(money.get())


    month_payment = payment / months
    monthly_money.config(text=f"{month_payment:.2f}")
    result_text = "月份\t本金還款\t\t利息還款\t\t剩餘本金\n"

    if var.get():
        early_repayment_money = int(early_repayment_amount.get())
        early_repayment_month = int(early_repayment_time.get())

    for month in range(1, months + 1):
        interest_payment = payment * months_rate
        term.append(month)
        ins.append(interest_payment)
        prin.append(month_payment)

        if var.get() and month == early_repayment_month:
            month_payment = early_repayment_money
            payment -= early_repayment_money
            monthly_payment = (payment * months_rate) / (1 - (1 + months_rate) ** -(months - month))
            early_repaymentLabel_monthly_money.config(text=f"{monthly_payment:.2f}")
        else:
            payment -= month_payment

        result_text += f"{month}\t{month_payment:.0f}\t\t{interest_payment:.0f}\t\t{payment:.0f}\n"

    plt.clf()
    plt.plot(term, ins,prin)
    plt.legend(['interest','principal'])
    plt.xlabel("months")
    plt.ylabel("NTD dollars")
    plt.show()

    result.delete(1.0, END)
    result.insert(END, result_text)



def clearall():
    Erate.delete(0, END)
    Eyear.delete(0, END)
    Eloan.delete(0, END)
    early_repayment_amount.delete(0, END)
    early_repayment_time.delete(0, END)
    early_repayment_amount.config(state=DISABLED)
    early_repayment_time.config(state=DISABLED)
    var.set(0)
    result.delete(1.0, END)
    monthly_money.config(text="")
    early_repaymentLabel_monthly_money.config(text="")
    lslider.set(0)
    mslider.set(0)
    rslider.set(0)



pw = PanedWindow(win, orient=HORIZONTAL)
pw.pack(fill=BOTH, expand=True)

leftframe = LabelFrame(pw, text="資料輸入區")
pw.add(leftframe)
rightframe = LabelFrame(pw, text="滑桿選擇區")
pw.add(rightframe)

Label(leftframe, text="貸款年利率(%):", width=20, anchor="w").grid(row=0, column=0, sticky="w", pady=5)
Label(leftframe, text="貸款年數:", width=20, anchor="w").grid(row=1, column=0, sticky="w", pady=5)
Label(leftframe, text="貸款金額:", width=20, anchor="w").grid(row=2, column=0, sticky="w", pady=5)
Label(leftframe, text="提前還款:", width=20, anchor="w").grid(row=3, column=0, sticky="w", pady=5)
Label(leftframe, text="提前還款時間(月數):", width=20, anchor="w").grid(row=4, column=0, sticky="w", pady=5)
Label(leftframe, text="提前還款金額:", width=20, anchor="w").grid(row=5, column=0, sticky="w", pady=5)
Label(leftframe, text="提前還款前月付款:", width=20, anchor="w").grid(row=6, column=0, sticky="w", pady=5)
Label(leftframe, text="提前還款後月付款:", width=20, anchor="w").grid(row=7, column=0, sticky="w", pady=5)

interest_rate = StringVar()
Erate = Entry(leftframe, textvariable=interest_rate, justify=RIGHT)
Erate.grid(row=0, column=1, pady=5)
years = StringVar()
Eyear = Entry(leftframe, textvariable=years, justify=RIGHT)
Eyear.grid(row=1, column=1, pady=5)
money = StringVar()
Eloan = Entry(leftframe, textvariable=money, justify=RIGHT)
Eloan.grid(row=2, column=1, pady=5)

var = IntVar()
early_repayment_check = Checkbutton(leftframe, variable=var, command=toggle_early_repayment)
early_repayment_check.grid(row=3, column=1, pady=5)
early_repayment_time = Entry(leftframe, width=20, justify="right", state=DISABLED)
early_repayment_time.grid(row=4, column=1, pady=5)
early_repayment_amount = Entry(leftframe, width=20, justify="right", state=DISABLED)
early_repayment_amount.grid(row=5, column=1, pady=5)
monthly_money = Label(leftframe, text="", width=20)
monthly_money.grid(row=6, column=1, pady=5)
early_repaymentLabel_monthly_money = Label(leftframe, text="", width=20)
early_repaymentLabel_monthly_money.grid(row=7, column=1, pady=5)

calculate_btn = Button(leftframe, text="計算貸款金額", command=cal)
calculate_btn.grid(row=8, column=0, pady=10)
clear_btn = Button(leftframe, text="清除", command=clearall)
clear_btn.grid(row=8, column=1, pady=10)
result = Text(leftframe, height=20, width=70)
result.grid(row=9, columnspan=4)


lslider = Scale(rightframe, from_=20, to=0, orient=VERTICAL, command=fill)
lslider.grid(row=1, column=0)
mslider = Scale(rightframe, from_=100, to=0, orient=VERTICAL, command=fill)
mslider.grid(row=1, column=1)
rslider = Scale(rightframe, from_=100000000, to=0, orient=VERTICAL, command=fill)
rslider.grid(row=1, column=2)


Eyear.bind("<KeyRelease>", update_slider_from_entry)
Eloan.bind("<KeyRelease>", update_slider_from_entry)
Erate.bind("<KeyRelease>", update_slider_from_entry)

var1 =  IntVar()
var1.set(1)
rbtn1 = Radiobutton(rightframe, text="本息平均攤還法", variable=var1, value=1, command=cal)
rbtn2 = Radiobutton(rightframe, text="本金平均攤還法", variable=var1, value=2, command=cal2)
rbtn1.grid(row=2, column=3, sticky=E, padx=3)
rbtn2.grid(row=3, column=3, sticky=E, padx=3)

win.mainloop()

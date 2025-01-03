from tkinter import *
from tkinter import messagebox

win = Tk()
win.title("購物車")
win.geometry("400x300")

shopping_cart = {}

Label(win, text="商品名稱:").grid(row=0, column=0, padx=10, pady=10)
item_input = Entry(win, width=20)
item_input.grid(row=0, column=1)

Label(win, text="商品數量:").grid(row=1, column=0, padx=10, pady=10)
quantity_input = Entry(win, width=10)
quantity_input.grid(row=1, column=1)

cart_display = Text(win, height=10, width=30, state='disabled')
cart_display.grid(row=3, column=0, columnspan=2, pady=10)

total_label = Label(win, text="總數量: 0", font=("Arial", 12))
total_label.grid(row=4, column=0, columnspan=2, pady=10)

def add_to_cart():
    item = item_input.get().strip()
    try:
        quantity = int(quantity_input.get().strip())
        
        if item == "":
            messagebox.showerror("輸入錯誤", "請輸入有效的商品名稱")
            return
        
        if quantity <= 0:
            messagebox.showerror("輸入錯誤", "數量必須大於0")
            return

        if item in shopping_cart:
            shopping_cart[item] += quantity
        else:
            shopping_cart[item] = quantity
        
        update_cart_display()  
        update_total_quantity()  
        

        item_input.delete(0, END)
        quantity_input.delete(0, END)
    
    except ValueError:
        messagebox.showerror("輸入錯誤", "請輸入有效的數量")


def update_cart_display():
    cart_display.config(state='normal')  
    cart_display.delete(1.0, END)  
    for item, quantity in shopping_cart.items():
        cart_display.insert(END, f"{item}: {quantity}\n")
    cart_display.config(state='disabled')  

def update_total_quantity():
    total_quantity = sum(shopping_cart.values())
    total_label.config(text=f"總數量: {total_quantity}")

add_button = Button(win, text="添加", command=add_to_cart)
add_button.grid(row=2, column=0, columnspan=2, pady=10)

win.mainloop()

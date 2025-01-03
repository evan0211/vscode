from tkinter import *

counter = 0                                
def run_counter(digit):                    
    def counting():                         
        global counter
        if counter == 100:
            return countdown()
        counter += 1                       
        digit.config(text=str(counter))
        digit.after(100,counting)         
    def countdown():                         
        global counter
        if counter == 0:
            return counting()
        counter -= 1                       
        digit.config(text=str(counter))
        digit.after(100,countdown)         
    counting()                    
                                

win = Tk()
win.title("ch2_23")
digit=Label(win,bg="yellow",fg="blue",    
            height=3,width=10,             
            font=("Helvetic" ,20,"bold"))      
digit.pack()
run_counter(digit)                         

win.mainloop()
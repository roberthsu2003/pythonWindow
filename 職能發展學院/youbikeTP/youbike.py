import dataSource
import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        #上方的Frame=========start
        topFrame = tk.Frame(self,background='red')
        tk.Label(topFrame,text="台北市youbike即時監測系統",font=("arial",20)).pack()
        topFrame.grid(column=0,row=0,padx=20,pady=20)
        #上方的Frame=========end

if __name__=="__main__":
    dataSource.update_youbike_data()
    window = Window()
    window.title("台北市youbike及時監測資料")
    window.mainloop()

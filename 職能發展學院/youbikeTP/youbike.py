import dataSource
import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        #上方的Frame=========start
        topFrame = tk.Frame(self,background='red')
        tk.Label(topFrame,text="台北市youbike即時監測系統",font=("arial",20)).pack()
        topFrame.grid(column=0,row=0,columnspan=3,padx=20,pady=20)
        #上方的Frame=========end
        leftBottom = tk.LabelFrame(self,background='blue')
        tk.Label(leftBottom, text="正常租借站點", font=("arial", 20)).pack()
        leftBottom.grid(column=0,row=1,padx=20,pady=20)

        centerBottom = tk.LabelFrame(self,background='gray')
        tk.Label(centerBottom, text="將無車可借站點", font=("arial", 20)).pack()
        centerBottom.grid(column=1,row=1,padx=20,pady=20)

        rightBottom = tk.LabelFrame(self, background='green')
        tk.Label(rightBottom, text="將無法還車站點", font=("arial", 20)).pack()
        rightBottom.grid(column=2, row=1, padx=20, pady=20)

if __name__=="__main__":
    dataSource.update_youbike_data()
    window = Window()
    window.title("台北市youbike及時監測資料")
    window.mainloop()

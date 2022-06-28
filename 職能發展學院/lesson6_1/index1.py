import tkinter.ttk as ttk
import os
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from PIL import ImageTk, Image

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("台積電當日線圖")
        mainFrame  = tk.Frame(self, relief="groove", borderwidth=2)
        titleFrame = tk.Frame(mainFrame)
        tk.Label(titleFrame,text="台積電當日線圖",font=("Arial",20,'bold'),fg="#555555").pack(padx=10)
        titleFrame.pack(pady=30)
        mainFrame.pack(pady=30,padx=30,ipadx=30,ipady=30)
        #-----------建立顯示畫面-----------------------
        self.panel = tk.Label(self)
        self.panel.pack(side = "bottom", fill = "both", expand = "yes")
        self.repeatRun()

    def repeatRun(self):
        print("Hello!")
        self.after(1000,self.repeatRun)

def closeWindow():
    print("close window")
    window.destroy()



if __name__ == "__main__":
    window = Window()
    window.resizable(width=0,height=0)
    window.protocol("WM_DELETE_WINDOW",closeWindow)
    window.mainloop()





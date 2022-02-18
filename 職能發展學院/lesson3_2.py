#!usr/bin/python3.8
"""
這是我的python_window範例
"""
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        labelFont = tkFont.Font(family="Arial", size=30)
        label = ttk.Label(self,text='Hello World',font=labelFont,anchor=tk.CENTER)
        label.pack(padx=20,pady=10)
        leftbutton = ttk.Button(self,text="確定")
        leftbutton.pack(side=tk.LEFT,pady=10,ipady=10,padx=20)
        rightbutton = ttk.Button(self, text="取消")
        rightbutton.pack(side=tk.RIGHT, pady=10, ipady=10,padx=20)



if __name__ == "__main__":
    window = Window()
    window.title('class的寫法')
    #window.geometry('300x300')
    window.config(bg='blue')
    window.mainloop()
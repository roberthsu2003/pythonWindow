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
        labelFont = tkFont.Font(family="Lucida Grande", size=30)
        label = ttk.Label(self,text='Hello World',font=labelFont)
        label.pack()



if __name__ == "__main__":
    window = Window()
    window.title('class的寫法')
    window.geometry('300x300')
    window.config(bg='blue')
    window.mainloop()
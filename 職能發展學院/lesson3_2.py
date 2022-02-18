#!usr/bin/python3.8
"""
這是我的python_window範例
"""
import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        label = ttk.Label(self,text='Hello World')
        label.pack()



if __name__ == "__main__":
    window = Window()
    window.title('class的寫法')
    window.geometry('300x300')
    window.config(bg='blue')
    window.mainloop()
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_16")
        self.geometry("300x200")
        fm = Frame(self)
        Button(fm, text='side=TOP, anchor=W').pack(side=TOP,expand=YES, anchor=W)
        Button(fm, text='side=TOP, anchor=W').pack(side=TOP,expand=YES, anchor=W)
        Button(fm, text='side=TOP, anchor=W').pack(side=TOP,expand=YES, anchor=W)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
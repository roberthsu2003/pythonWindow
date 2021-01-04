import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_19")

        fm = Frame(self)
        Button(fm, text='TOP').pack(side=TOP,expand=YES, anchor=W,fill=X)
        Button(fm, text='CENTER').pack(side=TOP,expand=YES, anchor=W,fill=X)
        Button(fm, text='Bottom').pack(side=TOP,expand=YES, anchor=W,fill=X)
        fm.pack(side=LEFT, fill=BOTH, expand=YES)

        fm1 = Frame(self)
        Button(fm1, text='LEFT').pack(side=LEFT)
        Button(fm1, text='This is Center Button').pack(side=LEFT)
        Button(fm1, text='Right').pack(side=LEFT)
        fm1.pack(side=LEFT, padx=10)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
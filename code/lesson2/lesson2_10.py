import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_10")
        self.geometry("300x200")

        fm = Frame(self)
        Button(self, text='Top').pack(side=TOP, fill=X)
        Button(self, text='Center').pack(side=TOP, fill=X)
        Button(self, text='Bottom').pack(side=TOP, fill=X)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
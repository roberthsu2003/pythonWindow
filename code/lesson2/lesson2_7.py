import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_7")
        self.geometry("300x200")

        fm = Frame(self)
        Button(self, text='Left').pack(side=LEFT, expand=YES)
        Button(self, text='Center').pack(side=LEFT, expand=YES)
        Button(self, text='Right').pack(side=LEFT, expand=YES)
        fm.pack(fill=BOTH, expand=YES)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
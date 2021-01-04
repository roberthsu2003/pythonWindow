import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("lesson2_1")

        Button(self, text='Left').pack(side=LEFT)
        Button(self, text='Center').pack(side=LEFT)
        Button(self, text='Right').pack(side=LEFT)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
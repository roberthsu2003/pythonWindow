from tkinter import messagebox
import tkinter as tk
from tkinter import *

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.option_add('*font',('verdana', 12, 'bold'))
        self.title("messagebox")

        Button(self, text='showinfo', padx=10,pady=10,command=lambda :messagebox.showinfo("information","Infomative message")).pack(side=LEFT,padx=30,pady=30)
        Button(self, text='showError', padx=10,pady=10,command=lambda : messagebox.showerror("Error","Error message")).pack(side=LEFT,padx=30,pady=30)
        Button(self, text='showWarning', padx=10,pady=10,command=lambda :messagebox.showwarning("Warning","Warning message")).pack(side=LEFT,padx=30,pady=30)

if __name__ == "__main__":
    window = Window()
    window.mainloop()

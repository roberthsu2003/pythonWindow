import tkinter as tk

class Dialog(tk.Toplevel):
    def __init__(self,root,title):
        super().__init__(root)
        self.transient(root)
        self.geometry('600x300')
        tk.Label(self,text=title).pack()
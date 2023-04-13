import tkinter as tk
from tkinter import ttk

class MapDisplay(tk.Toplevel):
    def __init__(self,master,data_dict,**kwargs):
        super().__init__(master,**kwargs)
        closeButton = ttk.Button(self,text="close")
        closeButton.pack(padx=30,pady=30)
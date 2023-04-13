import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog

class MapDisplay(Dialog):
    def __init__(self,master,data_dict,**kwargs):
        super().__init__(master,**kwargs)
        
    
    #override
    def body(self,master):
        closeButton = ttk.Button(self,text="close")
        closeButton.pack(padx=30,pady=30)
    #override
    
    def buttonbox(self):
        pass

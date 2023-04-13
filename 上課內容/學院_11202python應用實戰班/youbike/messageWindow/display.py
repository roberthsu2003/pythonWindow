import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import Dialog

class MapDisplay(Dialog):
    def __init__(self,master,data_dict,**kwargs):
        super().__init__(master,**kwargs)
        
    
    #override
    def body(self,master):
        pass
        
    #override
    def buttonbox(self):
        '''add standard button box.
        override if you do not want the standard buttons
        '''

        boxFrame = ttk.Frame(self)
        button = ttk.Button(boxFrame, text="關閉", width=10, command=self.ok, default=tk.ACTIVE) #self.ok方法是繼承來的
        button.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", self.ok)
        boxFrame.pack()


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class TopFrame(ttk.LabelFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        flowerImage1 = Image.open("./images/flower1.png")
        self.flowerPhoto1 = ImageTk.PhotoImage(flowerImage1)
        canvas = tk.Canvas(self, width=173, height=200)
        canvas.pack()
        canvas.create_image(0,0,image=self.flowerPhoto1,anchor='nw')
        canvas.create_text(0,200,text='Flower', fill='yellow', font=('verdana', 36),anchor='sw')
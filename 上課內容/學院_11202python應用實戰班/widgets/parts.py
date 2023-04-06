import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class TopFrame(ttk.LabelFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        flowerImage1 = Image.open("./images/flower1.png")
        self.flowerPhoto1 = ImageTk.PhotoImage(flowerImage1)
        self.canvas = tk.Canvas(self, width=500, height=200)
        self.canvas.pack()
        self.canvas.create_image(0,5,image=self.flowerPhoto1,anchor='nw')
        self.canvas.create_text(0,200,text='Flower', fill='yellow', font=('verdana', 36),
        anchor='sw')

        diamondImage1 = Image.open("./images/diamond.png")
        self.diamondPhoto1 = ImageTk.PhotoImage(diamondImage1)
        self.canvas.create_image(175,5,image=self.diamondPhoto1,anchor='nw')

        atomImage1 = Image.open("./images/atom.png")
        self.atomPhoto1 = ImageTk.PhotoImage(atomImage1)
        self.canvas.create_image(280,5,image=self.atomPhoto1,anchor='nw')



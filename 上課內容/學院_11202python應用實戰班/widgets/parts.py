import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class TopFrame(ttk.LabelFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        #using ttk.Style to change the style of the self widget
        ttkStyle = ttk.Style()
        ttkStyle.theme_use('default')
        flowerImage1 = Image.open("./images/flower1.png")
        self.flowerPhoto1 = ImageTk.PhotoImage(flowerImage1)
        self.canvas = tk.Canvas(self, width=173, height=200)
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

        #created ttk.scrollbar of tkinter in canvas
        self.scrollbar = ttk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.scrollbar.pack(side='bottom', fill='x')
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.canvas.configure(scrollregion=(0,0,500,200))





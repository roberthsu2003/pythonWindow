import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
#create canvas with tkinter
#How to draw images in tkinter window

def createImageOfTkinterUsingPIL():
    pass

    
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        topFrame = ttk.LabelFrame(self)
        flowerImage1 = Image.open("./images/flower1.png")
        self.flowerPhoto1 = ImageTk.PhotoImage(flowerImage1)
        canvas = tk.Canvas(topFrame, width=173, height=200)
        canvas.pack()
        canvas.create_image(0,0,image=self.flowerPhoto1,anchor='nw')
        canvas.create_text(0,200,text='Flower', fill='yellow', font=('verdana', 36),anchor='sw')
        topFrame.pack()
        

def main():
    window = Window()
    window.title("Widgets")
    window.mainloop()

if __name__ == "__main__":
    main()
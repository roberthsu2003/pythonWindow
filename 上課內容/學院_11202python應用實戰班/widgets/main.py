import tkinter as tk
from tkinter import ttk
#create canvas with tkinter
#How to draw images in tkinter window

def DrawImageWithTkinter():
    root = tk.Tk()
    root.title("Drawing an Image")
    root.geometry("400x400")
    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack()
    img = tk.PhotoImage(file="image.png")
    canvas.create_image(20, 20, anchor=tk.NW, image=img)
    root.mainloop()

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        topFrame = ttk.LabelFrame(self)
        canvas = tk.Canvas(topFrame, width=400, height=400)
        canvas.pack()
        topFrame.pack()
        

def main():
    window = Window()
    window.title("Widgets")
    window.mainloop()

if __name__ == "__main__":
    main()
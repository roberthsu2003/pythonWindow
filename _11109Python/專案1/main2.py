import tkinter as tk
from PIL import Image, ImageTk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        bgImage = Image.open('bg.jpg')        
        self.tkImage = ImageTk.PhotoImage(bgImage)
        mainCanvas = tk.Canvas(self)        
        mainCanvas.create_image(0,0,anchor=tk.NW,image=self.tkImage)
        tk.Button(mainCanvas,text="click").pack()     
        mainCanvas.pack(fill=tk.BOTH, expand=True)
        

def main():
    window = Window()
    window.title("Frame框架")
    window.geometry("640x427")
    window.mainloop()

if __name__ == "__main__":
    main()
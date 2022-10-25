import tkinter as tk
from PIL import Image, ImageTk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        #----建立背景------------
        bgImage = Image.open('bg.jpg')        
        self.tkImage = ImageTk.PhotoImage(bgImage)
        mainCanvas = tk.Canvas(self)        
        mainCanvas.create_image(0,0,anchor=tk.NW,image=self.tkImage)            
        mainCanvas.pack(fill=tk.BOTH, expand=True)
        #end----建立背景------------

def main():
    window = Window()
    window.title("Frame框架")
    window.resizable(0,0) #可以使用滑鼠改變視窗的大小
    window.geometry("640x427+300+200")#設定window的大小和位置
    window.mainloop()

if __name__ == "__main__":
    main()
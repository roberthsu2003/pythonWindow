import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        ttkStyle = ttk.Style()
        #print(ttkStyle.theme_names())
        ttkStyle.theme_use('classic')
        ttkStyle.configure('white.TLabelFrame',background='white')

        drawingFrame = ttk.LabelFrame(self,text="這裏是畫圖區",style='white.TLabelFrame')
        drawingFrame.pack(padx=50,pady=50)
        lineCanvas = tk.Canvas(drawingFrame,width=100,height=30)
        lineCanvas.create_line((0,0),(100,0),width=30,fill='red')
        lineCanvas.pack()
        ovalCanvas = tk.Canvas(drawingFrame,width=110,height=110)
        ovalCanvas.create_oval((10,10),(100,100),width=10,outline='red',fill='purple')
        ovalCanvas.pack()




def main():
    window = Window()
    window.title('畫圖')
    window.mainloop()

if __name__ == "__main__":
    main()
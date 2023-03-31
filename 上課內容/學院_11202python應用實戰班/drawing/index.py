import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        ttkStyle = ttk.Style()
        #print(ttkStyle.theme_names())
        ttkStyle.theme_use('default')
        ttkStyle.configure('white.TLabelframe',background='white',bd=0)
        ttkStyle.configure('white.TLabelframe.Label',background='white',foreground='red')
        f1 = tkFont.Font(family='Helvetica', size=16, weight='bold')
        
        
        drawingFrame = ttk.LabelFrame(self,text="這裏是畫圖區",style='white.TLabelframe')
        drawingFrame.pack(padx=50,pady=50)

        lineCanvas = tk.Canvas(drawingFrame,width=100,height=30,bd=0,highlightthickness=0,background='white')        
        lineCanvas.create_line((0,0),(100,0),width=30,fill='red')
        lineCanvas.pack()

        ovalCanvas = tk.Canvas(drawingFrame,width=110,height=110,bd=0,highlightthickness=0,background='white')        
        ovalCanvas.create_oval((10,10),(100,100),width=10,outline='red',fill='purple')
        ovalCanvas.pack()

        textCanvas = tk.Canvas(drawingFrame,width=110,height=50,bd=0,highlightthickness=0,background='white')
        textCanvas.create_text(0,0,text="ABC_中文",font=f1,anchor='nw')
        textCanvas.pack()




def main():
    window = Window()
    window.title('畫圖')
    window.mainloop()

if __name__ == "__main__":
    main()
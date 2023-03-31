import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from PIL import Image,ImageTk

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

        mapCanvas = tk.Canvas(drawingFrame,width=300,height=300,bd=0,highlightthickness=0,background='white')
        taiwanImage = Image.open("map.png")
        newImage = taiwanImage.resize((300, 300),Image.LANCZOS)
        self.taiwanImageTk = ImageTk.PhotoImage(newImage)
        mapCanvas.create_image(0,0,image=self.taiwanImageTk,anchor=tk.NW)
        mapCanvas.create_text(100,100,text="ABC_中文",font=tkFont.Font(family='Helvetica', size=12),anchor='nw')
        mapCanvas.pack()



def main():
    window = Window()
    window.title('畫圖')
    window.mainloop()

if __name__ == "__main__":
    main()
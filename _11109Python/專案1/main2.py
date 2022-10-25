import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkFont

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

        #------建立Lable----------
        helv36 = tkFont.Font(family='Helvetica',size=36, weight='bold')
        tk.Label(mainCanvas,text="職能發展學院",font=helv36,background='#C9C8CD',foreground="#888888").place(x=370,y=50)
        #end------建立Lable----------

        #-----建立ButtonsFrame----------
        buttonFrame = tk.Frame(mainCanvas,background="#ffffff")
        buttonFrame.place(x=100,y=50)
        #end-----建立ButtonsFrame-------

        #-----建立Button-----
        bgImage1 = Image.open('icon1.png')
        self.tkImage1 = ImageTk.PhotoImage(bgImage1)
        btn1 = tk.Button(buttonFrame,image=self.tkImage1,borderwidth=0)
        btn1.pack(padx=10,pady=10)
        #end-----建立Button-----
        

def main():
    window = Window()
    window.title("Frame框架")
    window.resizable(0,0) #可以使用滑鼠改變視窗的大小
    window.geometry("640x427+300+200")#設定window的大小和位置
    window.mainloop()

if __name__ == "__main__":
    main()
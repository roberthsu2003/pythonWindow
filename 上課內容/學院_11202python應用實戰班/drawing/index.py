import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        drawingFrame = ttk.Labelframe(self,text="這裏是畫圖區")
        drawingFrame.pack(padx=50,pady=50)
        tk.Button(drawingFrame,text="Press Me",padx=10,pady=10).pack(padx=30,pady=20)



def main():
    window = Window()
    window.title('畫圖')
    window.mainloop()

if __name__ == "__main__":
    main()
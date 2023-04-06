import tkinter as tk
from parts import TopFrame,MedianFrame

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        topFrame = TopFrame(self,borderwidth=0)       
        topFrame.pack()
        medianFrame = MedianFrame(self,borderwidth=0)
        medianFrame.pack()
        

def main():
    window = Window()
    window.title("Widgets")
    window.mainloop()

if __name__ == "__main__":
    main()
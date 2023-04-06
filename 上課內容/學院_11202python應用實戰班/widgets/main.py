import tkinter as tk
from parts import TopFrame

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        topFrame = TopFrame(self)        
        topFrame.pack()
        

def main():
    window = Window()
    window.title("Widgets")
    window.mainloop()

if __name__ == "__main__":
    main()
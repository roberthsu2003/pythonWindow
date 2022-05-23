import tkinter as tk
from tkinter.font import Font

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("我的物件導向視窗")
        font = Font(size=25)
        label = tk.Label(self, text="Hello! World", bg="#cccccc",font=font)
        label.pack(padx=50,pady=100)




if __name__ == "__main__":
    window = Window()
    window.mainloop()
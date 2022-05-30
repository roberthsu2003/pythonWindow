import tkinter as tk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    root = Window()
    root.title("這是我的視窗")
    root.mainloop()
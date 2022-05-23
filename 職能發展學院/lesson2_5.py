import tkinter as tk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        print("我被執行")



if __name__ == "__main__":
    window = Window()
    window.mainloop()
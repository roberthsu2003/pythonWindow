import tkinter as tk
import tk_tools
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self):
        super().__init__();
        led = tk_tools.Led(self, size=50)
        led.to_red()
        led.to_green(on=True)
        led.grid()





if __name__ == "__main__":
    window = Window()
    window.mainloop()

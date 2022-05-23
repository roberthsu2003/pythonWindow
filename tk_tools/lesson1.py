import tkinter as tk
import tk_tools
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self):
        super().__init__();

        rs = tk_tools.RotaryScale(self,
                                  max_value=100.0,
                                  size=200,
                                  unit='km/h')
        rs.grid(row=0, column=0)
        rs.set_value(60)




if __name__ == "__main__":
    window = Window()
    window.mainloop()

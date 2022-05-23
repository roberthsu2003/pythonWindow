import tkinter as tk
import tk_tools
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self):
        super().__init__();
        gauge = tk_tools.Gauge(self,
                               width=400,
                               height=200,
                               min_value=0.0,
                               max_value=50.0,
                               yellow=60,
                               red=80,
                               yellow_low=0,
                               red_low=0,
                               label='數值', unit='')
        gauge.grid()
        gauge.set_value(35.55)




if __name__ == "__main__":
    window = Window()
    window.mainloop()

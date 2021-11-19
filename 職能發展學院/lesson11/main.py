import tkinter as tk
import dataSource

class Window(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title = "全省空氣品質指標"
        dataSource.getAirData()

if __name__ == "__main__":
    window = Window()
    window.mainloop()
import tkinter as tk
import dataSource
from tkinter import messagebox

class Window(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title = "全省空氣品質指標"
        try:
            downloadData = dataSource.getAirData()
        except ValueError as e:
            messagebox.showwarning("連線錯誤",e)
            self.destroy()

        print(downloadData)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
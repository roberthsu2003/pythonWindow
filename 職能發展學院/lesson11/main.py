import tkinter as tk
import dataSource
from tkinter import messagebox

class Window(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title = "全省空氣品質指標"
        if dataSource.getAirData() is not None:
            print("下載成功")
        else:
            messagebox.showerror("連線錯誤","請稍後再試")

if __name__ == "__main__":
    window = Window()
    window.mainloop()
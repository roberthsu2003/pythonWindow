import datasource
import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        topFrame = ttk.LabelFrame(self,text="台北市行政區")
        length = len(datasource.sarea_list)
        for i in range(length):
            cols = i % 3
            rows = i // 3
            ttk.Radiobutton(topFrame,text=datasource.sarea_list[i]).grid(column=cols,row=rows)

        topFrame.pack()

def main():
    window = Window()
    window.title("台北市youbike2.0資訊")
    window.mainloop()

if __name__ == "__main__":
    main()
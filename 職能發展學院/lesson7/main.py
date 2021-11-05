from datasource import getStackData
import tkinter as tk

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        name, allDataList = getStackData(2303)
        print(name)
        for item in allDataList:
            print(item)


if __name__ == "__main__":
    window = Window()
    window.mainloop()


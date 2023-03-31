import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
from tools import Taiwan_AQI

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        aqi_data = Taiwan_AQI()
        bad5 = aqi_data.get_bad(n=5)
        for item in bad5:
            print(item)

        good5 = aqi_data.get_better(n=5)
        for item in good5:
            print(item)


def main():
    window = Window()
    window.title('畫圖')
    window.mainloop()

if __name__ == "__main__":
    main()
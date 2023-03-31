import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
from tools import Taiwan_AQI

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        aqi_data = Taiwan_AQI()
        bad3 = aqi_data.get_bad_3()
        for item in bad3:
            print(item)


def main():
    window = Window()
    window.title('畫圖')
    window.mainloop()

if __name__ == "__main__":
    main()
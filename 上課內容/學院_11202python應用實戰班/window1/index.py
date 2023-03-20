import tkinter as tk
from tkinter import Button

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        btn1 = Button(self,text="按鈕1")
        btn1.pack()

        btn2 = Button(self,text="按鈕2")
        btn2.pack()


def main():
    window = Window()
    window.title("這是第一個視窗")
    window.geometry("400x300")
    window.mainloop()

if __name__ == "__main__":
    main()
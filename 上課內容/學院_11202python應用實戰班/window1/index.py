import tkinter as tk
from tkinter import Button

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Button(self,text="按鈕1",padx=10,pady=10).pack()
        Button(self,text="按鈕2",padx=10,pady=10).pack()
        


def main():
    window = Window()
    window.title("這是第一個視窗")
    window.geometry("400x300")
    window.mainloop()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import Button

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Button(self,text="按鈕1",font=('Helvetica', '24'),pady=10).pack(fill=tk.X)
        Button(self,text="按鈕2",font=('Helvetica', '24'),pady=10).pack(fill=tk.X)
        


def main():
    window = Window()
    window.title("這是第一個視窗")
    window.geometry("400x300")
    window.mainloop()

if __name__ == "__main__":
    main()
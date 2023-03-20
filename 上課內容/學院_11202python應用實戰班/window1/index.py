import tkinter as tk
from tkinter import Button,Frame

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Button(self,text="按鈕1",font=('Helvetica', '24'),pady=10,command=self.btn1_click).pack(fill=tk.X)
        Button(self,text="按鈕2",font=('Helvetica', '24'),pady=10,command=self.btn2_click).pack(fill=tk.X)

        bottom_frame  = Frame(self,bg="#ffffff")
        Button(bottom_frame,text="按鈕3",font=('Helvetica', '24')).pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        Button(bottom_frame,text="按鈕4",font=('Helvetica', '24')).pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        Button(bottom_frame,text="按鈕5",font=('Helvetica', '24')).pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        bottom_frame.pack(expand=True,fill=tk.BOTH)

    def btn1_click(self):
        print("按鈕1按下")

    def btn2_click(self):
        print("按鈕2按下")
        


def main():
    window = Window()
    window.title("這是第一個視窗")
    window.geometry("400x300")
    window.mainloop()

if __name__ == "__main__":
    main()
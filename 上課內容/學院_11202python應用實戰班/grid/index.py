'''
專案在學習grid的編排
'''

import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        ttkStyle = ttk.Style()
        ttkStyle.configure('1.main_bg_Color',background='#ffffff')
        mainFrame  =  ttk.Frame(self,style='1.main_bg_Color')
        mainFrame.pack(expand=True,fill=tk.BOTH)


def main():
    '''
    這是程式的執行點
    '''
    window = Window()
    window.title("BMI計算")
    window.geometry("400x500")
    window.mainloop()

if __name__ == "__main__":
    main()
'''
專案在學習grid的編排
'''

import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        ttkStyle = ttk.Style()
        print(ttkStyle.theme_names())
        ttkStyle.theme_use('default')
        ttkStyle.configure('red.TFrame',background='#ff0000')
        ttkStyle.configure('white.TFrame',background='#ffffff')
        ttkStyle.configure('yellow.TFrame',background='yellow')
        
        mainFrame = ttk.Frame(self,style='red.TFrame')        
        mainFrame.pack(expand=True,fill=tk.BOTH)
        

        topFrame = ttk.Frame(mainFrame,style='white.TFrame',height=100)
        topFrame.pack(fill=tk.X)

        bottomFrame = ttk.Frame(mainFrame,style='yellow.TFrame')
        bottomFrame.pack(expand=True,fill=tk.BOTH)


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
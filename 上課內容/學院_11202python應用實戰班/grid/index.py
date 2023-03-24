'''
專案在學習grid的編排
'''

import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        ttkStyle = ttk.Style()
        ttkStyle.configure('back.TFrame',background='#ffffff')
        
        mainFrame = ttk.Frame(self,style='back.TFrame')        
        mainFrame.pack(expand=True,fill=tk.BOTH)
        

        topFrame = ttk.Frame(mainFrame,style='back.TFrame',height=100)
        topFrame.pack(fill=tk.X)

        bottomFrame = ttk.Frame(mainFrame,style='back.TFrame')
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
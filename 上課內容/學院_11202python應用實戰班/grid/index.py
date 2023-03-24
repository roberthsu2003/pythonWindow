'''
專案在學習grid的編排
'''

import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        ttkStyle = ttk.Style()
        ttkStyle.theme_use('default')
        ttkStyle.configure('red.TFrame',background='#ff0000')
        ttkStyle.configure('white.TFrame',background='#ffffff')
        ttkStyle.configure('yellow.TFrame',background='yellow')
        ttkStyle.configure('white.TLabel',background='#ffffff')
        ttkStyle.configure('gridLabel.TLabel',font=('Helvetica', 16))
        ttkStyle.configure('gridEntry.TEntry',font=('Helvetica', 16))
        
        mainFrame = ttk.Frame(self)        
        mainFrame.pack(expand=True,fill=tk.BOTH)
        

        topFrame = ttk.Frame(mainFrame,height=100)
        topFrame.pack(fill=tk.X)

        ttk.Label(topFrame,text="BMI試算",font=('Helvetica', '20')).pack(pady=20)

        bottomFrame = ttk.Frame(mainFrame,style='yellow.TFrame')
        bottomFrame.pack(expand=True,fill=tk.BOTH)
        bottomFrame.columnconfigure(0,weight=3)
        bottomFrame.columnconfigure(1,weight=5)
        bottomFrame.rowconfigure(0, weight=1)
        

        ttk.Label(bottomFrame,text="姓名:",style='gridLabel.TLabel').grid(column=0,row=0,sticky=tk.E)
        nameEntry = ttk.Entry(bottomFrame,style='gridEntry.TEntry')
        nameEntry.grid(column=1,row=0,sticky=tk.W)

        ttk.Label(bottomFrame,text="出生年月日:",style='gridLabel.TLabel').grid(column=0,row=1,sticky=tk.E)
        ttk.Label(bottomFrame,text="(2000/03/01)",style='gridLabel.TLabel').grid(column=0,row=2,sticky=tk.E)

        birthEntry = ttk.Entry(bottomFrame,style='gridEntry.TEntry')
        birthEntry.grid(column=1,row=1,sticky=tk.W,rowspan=2)

        ttk.Label(bottomFrame,text="身高(cm):",style='gridLabel.TLabel').grid(column=0,row=3,sticky=tk.E)
        heightEntry = ttk.Entry(bottomFrame,style='gridEntry.TEntry')
        heightEntry.grid(column=1,row=3,sticky=tk.W)

        ttk.Label(bottomFrame,text="體重(kg):",style='gridLabel.TLabel').grid(column=0,row=4,sticky=tk.E)
        weightEntry = ttk.Entry(bottomFrame,style='gridEntry.TEntry')
        weightEntry.grid(column=1,row=4,sticky=tk.W)
        





def main():
    '''
    這是程式的執行點
    '''
    window = Window()
    window.title("BMI計算")
    #window.geometry("400x500")
    window.mainloop()

if __name__ == "__main__":
    main()
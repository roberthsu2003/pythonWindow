'''
專案在學習grid的編排
'''

import tkinter as tk
from tkinter import ttk
import re
from PIL import Image,ImageTk

class Window(tk.Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        ttkStyle = ttk.Style()
        ttkStyle.theme_use('default')
        ttkStyle.configure('red.TFrame',background='#ff0000')
        ttkStyle.configure('white.TFrame',background='#ffffff')
        ttkStyle.configure('yellow.TFrame',background='yellow')
        ttkStyle.configure('white.TLabel',background='#ffffff')
        ttkStyle.configure('gridLabel.TLabel',font=('Helvetica', 16),foreground='#666666')
        ttkStyle.configure('gridEntry.TEntry',font=('Helvetica', 16))
        
        mainFrame = ttk.Frame(self)        
        mainFrame.pack(expand=True,fill=tk.BOTH,padx=30,pady=30)
        

        topFrame = ttk.Frame(mainFrame,height=100)
        topFrame.pack(fill=tk.X)

        ttk.Label(topFrame,text="BMI試算",font=('Helvetica', '20')).pack(pady=(80,20))

        bottomFrame = ttk.Frame(mainFrame)
        bottomFrame.pack(expand=True,fill=tk.BOTH)
        bottomFrame.columnconfigure(0,weight=3,pad=20)
        bottomFrame.columnconfigure(1,weight=5,pad=20)
        bottomFrame.rowconfigure(0, weight=1,pad=20)
        bottomFrame.rowconfigure(3, weight=1,pad=20)
        bottomFrame.rowconfigure(4, weight=1,pad=20)
        bottomFrame.rowconfigure(5, weight=1,pad=20)
        bottomFrame.rowconfigure(6, weight=1,pad=20)

        #定義entry的textvariable
        self.nameStringVar = tk.StringVar()
        self.birthStringVar = tk.StringVar()
        self.heightIntVar = tk.IntVar()
        self.weightIntVar = tk.IntVar()

        ttk.Label(bottomFrame,text="姓名:",style='gridLabel.TLabel').grid(column=0,row=0,sticky=tk.E)
        
        nameEntry = ttk.Entry(bottomFrame,style='gridEntry.TEntry',textvariable=self.nameStringVar)
        nameEntry.grid(column=1,row=0,sticky=tk.W,padx=10)

        ttk.Label(bottomFrame,text="出生年月日:",style='gridLabel.TLabel').grid(column=0,row=1,sticky=tk.E)
        ttk.Label(bottomFrame,text="(2000/03/01)",style='gridLabel.TLabel').grid(column=0,row=2,sticky=tk.E)

        birthEntry = ttk.Entry(bottomFrame,style='gridEntry.TEntry',textvariable=self.birthStringVar)
        birthEntry.grid(column=1,row=1,sticky=tk.W,rowspan=2,padx=10)

        ttk.Label(bottomFrame,text="身高(cm):",style='gridLabel.TLabel').grid(column=0,row=3,sticky=tk.E)
        heightEntry = ttk.Entry(bottomFrame,style='gridEntry.TEntry',textvariable=self.heightIntVar)
        heightEntry.grid(column=1,row=3,sticky=tk.W,padx=10)

        ttk.Label(bottomFrame,text="體重(kg):",style='gridLabel.TLabel').grid(column=0,row=4,sticky=tk.E)
        weightEntry = ttk.Entry(bottomFrame,style='gridEntry.TEntry',textvariable=self.weightIntVar)
        weightEntry.grid(column=1,row=4,sticky=tk.W,padx=10)

        self.messageText = tk.Text(bottomFrame,height=5,width=35,state=tk.DISABLED,takefocus=0,bd=0)
        self.messageText.grid(column=0,row=5,sticky=tk.N+tk.S,columnspan=2)

        #---------commitFrame開始--------------------
        #有左右2個按鈕
        #
        commitFrame = ttk.Frame(bottomFrame)
        commitFrame.grid(column=0,row=6,columnspan=2)
        commitFrame.columnconfigure(0,pad=10)
        commitBtn = ttk.Button(commitFrame,text="計算",command=self.press_commit)
        commitBtn.grid(column=0,row=0,sticky=tk.W)

        clearBtn = ttk.Button(commitFrame,text="清除",command=self.press_clear)
        clearBtn.grid(column=1,row=0,sticky=tk.E)
        #---------commitFrame結束--------------------

        #---------建立Logo--------------------
        logoImage = Image.open('logo.png')
        resizeImage = logoImage.resize((180,45),Image.LANCZOS)
        self.logoTkimage = ImageTk.PhotoImage(resizeImage)
        logoLabel = ttk.Label(self,image=self.logoTkimage,width=180)
        logoLabel.place(x=40,y=45)

    def press_clear(self) -> None:
        self.nameStringVar.set("")
        self.birthStringVar.set("")
        self.heightIntVar.set(0)
        self.weightIntVar.set(0)
        self.messageText.configure(state=tk.NORMAL)
        self.messageText.delete("1.0",tk.END)
        self.messageText.configure(state=tk.DISABLED)
        print("清除")

    def press_commit(self) -> None:
        self.check_data()

    def check_data(self) -> None:
        dateRegex = re.compile(r"^\d\d\d\d/\d\d/\d\d$")
        nameValue = self.nameStringVar.get()
        birthValue = self.birthStringVar.get()
        birthMatch = re.match(dateRegex,birthValue)
        if  birthMatch is None:            
            birthValue = ""

        try:
            heightValue = self.heightIntVar.get()
        except:
            heightValue = 0

        try:
            weightValue = self.weightIntVar.get()
        except:
            weightValue =  0
        
        if nameValue == "" or birthValue=="" or heightValue==0 or weightValue==0 :            
            self.messageText.configure(state=tk.NORMAL)
            self.messageText.delete("1.0",tk.END)
            self.messageText.insert(tk.END,"有欄位沒填或格式不正確")
            self.messageText.configure(state=tk.DISABLED)
        else:
            bmi = weightValue / (heightValue / 100) ** 2
            message = f"{nameValue}您好:\n"
            message += f"出生年月日:{birthValue}\n"
            message += f"BMI值是:{bmi:.2f}\n"
            message += f"狀態是:xxxx"

            self.messageText.configure(state=tk.NORMAL)
            self.messageText.delete("1.0",tk.END)
            self.messageText.insert(tk.END,message)
            self.messageText.configure(state=tk.DISABLED)

    



def close_window(w):
    w.destroy()        


def main():
    '''
    這是程式的執行點
    ''' 

    window = Window()
    window.title("BMI計算")
    window.resizable(width=False, height=False)
    window.protocol("WM_DELETE_WINDOW",lambda:close_window(window))
    window.mainloop()

if __name__ == "__main__":
    main()
from tkinter import messagebox
import tkinter.ttk as ttk

import tkinter as tk
class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("台積電,聯電,聯發科,鴻海歷史線圖")
        mainFrame  = tk.Frame(self, relief="groove", borderwidth=2)
        titleFrame = tk.Frame(mainFrame)
        tk.Label(titleFrame,text="台積電,聯電,聯發科,鴻海歷史線圖",font=("Arial",20,'bold'),fg="#555555").pack(padx=10)
        titleFrame.pack(pady=30)
        mainFrame.pack(pady=30,padx=30,ipadx=30,ipady=30)

        #-------------建立inputFrame-------------------
        self.inputFrame = tk.Frame(mainFrame,width=50)
        tk.Label(self.inputFrame, text="請選取股票號碼:",font=('Arial',13)).grid(row=0,column=0,sticky=tk.E)
        n = tk.StringVar()
        stock_choose = ttk.Combobox(self.inputFrame, width=27, textvariable=n)

        # Adding combobox drop down list
        stock_choose['values'] = ('2330.TW',
                                  '2303.TW',
                                  '2454.TW',
                                  '2317.TW',
                                  )

        stock_choose.grid(row=0, column=1, sticky=tk.E)

        self.inputFrame.pack()
        #-----------建立顯示畫面-----------------------







def closeWindow():
    print("close window")
    window.destroy()



if __name__ == "__main__":
    window = Window()
    window.resizable(width=0,height=0)
    window.protocol("WM_DELETE_WINDOW",closeWindow)
    window.mainloop()




